import re, os, urllib.request

def read(f):
    try:
        with open(f, 'rb') as f: 
            return f.read()
    except: 
        return b''

def links(d):
    l = re.findall(rb'https://[a-zA-Z0-9/_\.\-~=&?%]+\.webm', d)
    return list(dict.fromkeys(x.decode() for x in l))

def load_downloaded_links():
    cache_file = 'media/cache/downloaded_links.txt'
    if not os.path.exists(cache_file):
        return set()
    with open(cache_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def mark_as_downloaded(url):
    with open('media/cache/downloaded_links.txt', 'a', encoding='utf-8') as f:
        f.write(url + '\n')

def main():
    os.makedirs('media', exist_ok=True)
    os.makedirs('media/cache', exist_ok=True)
    
    downloaded_links = load_downloaded_links()
    cache_path = os.path.join(os.getenv('APPDATA'), 
                             "miHoYo/HYP/1_1/fedata/Cache/Cache_Data/data_1")
    lst = links(read(cache_path))
    
    print(f'发现 {len(lst)} 个WEBM链接')
    print(f'已跳过 {len(downloaded_links)} 个历史链接')

    for i, url in enumerate(lst, 1):
        if url in downloaded_links:
            continue
            
        final_path = f'media/{i}.webm'
        
        try:
            # ====== 1. HEAD 预检 (正确设置 headers 的方式) ======
            head_req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'},
                method='HEAD'
            )
            head_resp = urllib.request.urlopen(head_req, timeout=5)
            
            if 'video/' not in head_resp.headers.get('Content-Type', ''):
                print(f'x {i} 非视频文件 (跳过)')
                continue
                
            # ====== 2. 用 urlopen 正确下载 (直接写入目标路径) ======
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as resp, \
                 open(final_path, 'wb') as f:
                # 分块读取避免内存溢出
                while chunk := resp.read(8192):
                    f.write(chunk)
            
            # ====== 3. 立即更新记录 ======
            mark_as_downloaded(url)
            downloaded_links.add(url)
            print(f'✓ {i} 已下载')
            
        except Exception as e:
            print(f'x {i} 下载失败: {str(e)}')
            if os.path.exists(final_path):
                os.remove(final_path)  # 清理残次文件

if __name__ == '__main__':
    main()