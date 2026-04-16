import json
import re
import urllib.parse
from datetime import datetime
import csv
import os
import sys

# 输入参数
file_path = sys.argv[1] if len(sys.argv) > 1 else 'outbox.json'

if len(sys.argv) > 2:
    BASE_URL = sys.argv[2]
else:
    BASE_URL = input("请输入博客 URL（例如 https://example.com）：").strip()

BASE_URL = BASE_URL.rstrip("/")

try:
    if len(sys.argv) > 3:
        starting_post_id = int(sys.argv[3])
    else:
        starting_post_id = int(input("请输入起始文章编号：").strip())
except ValueError:
    print("起始编号必须是数字！")
    exit(1)


# 读取json文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 日期转换函数
def convert_date(date_str):
    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')

# 去除链接函数
def remove_specific_tags(content):
    # 1处理 hashtag：保留 #<span>xxx</span>
    a_pattern = re.compile(
        r'<a href="https?://[^/]+/tags/.*?" class="mention hashtag" rel="tag">(#<span>.*?</span>)</a>',
        re.DOTALL
    )
    content = re.sub(a_pattern, r'\1', content)
    # 2处理 @用户：保留 @<span>user</span>
    span_pattern = re.compile(
        r'<span class="h-card"[^>]*>\s*<a href="https?://[^/]+/@.*?" class="u-url mention">(@<span>.*?</span>)</a>\s*</span>',
        re.DOTALL
    )
    content = re.sub(span_pattern, r'\1', content)
    return content

# 去除html函数
def strip_p_tag(html):
    return re.sub(r'^<p>(.*?)</p>$', r'\1', html.strip(), flags=re.DOTALL)

# 判断私密性函数
def get_post_status(item, obj):
    PUBLIC = "https://www.w3.org/ns/activitystreams#Public"

    to = item.get("to", [])
    cc = item.get("cc", [])

    # 公开 or 不公开（unlisted）
    if PUBLIC in cc or PUBLIC in to:
        return "publish"

    # followers-only（也算公开给一部分人）
    if any("followers" in x for x in to):
        return "publish"

    # 剩下情况：
    # - 指定用户（私信）
    # - 只有自己可见
    return "private"


# 准备一个最终输出用的[]
result = []
current_id = starting_post_id

# Process each item in the JSON data
for item in data.get('orderedItems', []):
    # 跳过转嘟
    if item.get("type") != "Create":
        continue
    obj = item.get('object', {})
    if not isinstance(obj, dict):
        continue
    
    
    post_id = current_id
    post_date = convert_date(item.get('published'))
    post_date_gmt = convert_date(item.get('published'))
    post_status = get_post_status(item, obj)
    
    
    # 提取 id
    mastodon_url = obj.get("id") or item.get("id", "")
    mastodon_id = mastodon_url.rstrip("/").split("/")[-1]
    
    
    # 提取 conent
    post_content = obj.get('content', '')
    post_content = remove_specific_tags(post_content)
    
    if obj.get("inReplyTo"):
        reply_url = obj["inReplyTo"]
        post_content = f'<p>回复：<a href="{reply_url}">原帖</a></p>\n\n' + post_content
    
    
    # 提取 excerpt
    post_content_filtered = obj.get('summary', '') or ''
    post_content_filtered = remove_specific_tags(post_content_filtered)
    excerpt = post_content_filtered.strip()
    
    if not excerpt:
        # 去 HTML 标签
        text = re.sub(r'<.*?>', '', post_content)
        text = text.strip()
        suffix = "......（继续阅读）"
        limit = 100
        if len(text) > limit:
            excerpt = text[:limit - len(suffix)] + suffix
        else:
            excerpt = text
    
    
    # 提取 media
    content_media = []

    for att in obj.get("attachment", []):
        media_type = att.get("mediaType", "")
    
        if media_type.startswith("image") or media_type.startswith("video"):
            url = att.get("url", "")
            if url:
                filename = os.path.basename(url)
                title = os.path.splitext(filename)[0]
                full_url = f"{BASE_URL}/{filename}"

                content_media.append({
                    "type": "image" if media_type.startswith("image") else "video",
                    "url": full_url,
                    "title": title,
                    "filename": filename
                })
    
    content_images = [
        {
            "url": m["url"],
            "title": m["title"],
            "filename": m["filename"]
        }
        for m in content_media
    ]
    
    has_media = len(content_media) > 0
    
    
    # 提取 tag
    tags = []
    for t in obj.get("tag", []):
        if t.get("type") == "Hashtag":
            name = t.get("name", "")
            if name.startswith("#"):
                name = name[1:]  # 去掉 #
            if name:
                tags.append(name)
    
    # 有媒体
    if len(content_media) > 0:
        tags.append("有媒体")
    
    # 有折叠
    if post_content_filtered.strip():
        tags.append("有折叠")
    
    # 去重保序
    tags = list(dict.fromkeys(tags))
    tags_json = [{"name": t} for t in tags]
    
    
    
    # 拼接 conent+media
    media_blocks = ""

    for media in content_media:
        if media["type"] == "image":
            media_blocks += (
                f"<!-- wp:image -->\n"
                f"<figure class=\"wp-block-image size-full\">\n"
                f"<img src=\"{media['url']}\" alt=\"\" />\n"
                f"</figure>\n"
                f"<!-- /wp:image -->\n\n"
            )
        else:  # video
            media_blocks += (
                f"<!-- wp:video -->\n"
                f"<figure class=\"wp-block-video\">\n"
                f"<video controls src=\"{media['url']}\"></video>\n"
                f"</figure>\n"
                f"<!-- /wp:video -->\n\n"
            )
    
    final_content = ""

    if post_content_filtered:
        clean = strip_p_tag(post_content_filtered)
        final_content += f'<!-- wp:paragraph -->\n<p><em><strong>{clean}</strong></em></p>\n<!-- /wp:paragraph -->\n\n'

    if post_content:
        final_content += f'<!-- wp:paragraph -->\n{post_content}\n<!-- /wp:paragraph -->\n\n'

    final_content += media_blocks
    
    
    
    # 头图
    featured_image = None

    if content_media:
        # 找第一张图片
        first_image = next((m for m in content_media if m["type"] == "image"), None)

        if first_image:
            featured_image = {
                "url": first_image["url"],
                "title": first_image["title"],
                "filename": first_image["filename"]
            }
        else:
            # 全是视频
            featured_image = {
                "url": f"{BASE_URL}/video.png",
                "title": "video",
                "filename": "video.png"
            }



    # 生成最终 json
    post_json = {
        "ID": post_id,
        "post_title": str(post_id),
        "post_content": final_content.strip(),
        "post_excerpt": excerpt,
        "post_status": post_status,
        "post_type": "post",
        "post_author": 1,
        "post_date": post_date,
        "post_modified": post_date_gmt,
        "post_name": str(mastodon_id),
        "post_format": "standard",
        "tags": tags_json,
        "meta": [],
        "featured_image": featured_image,
        "content_images": content_images
    }

    result.append(post_json)
    current_id += 1


# OUTPUT
output_json_path = 'output.json'
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Data JSON has been written to {output_json_path}")
input("处理完成，按回车退出...")
