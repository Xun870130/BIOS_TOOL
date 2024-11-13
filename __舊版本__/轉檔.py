from PIL import Image

# 打開 GIF 文件
gif_path = r"D:\VScode\project\211\UI_image\pinOff.gif"
gif = Image.open(gif_path)

# 提取 GIF 的第一幀
gif.seek(0)

# 保存為 PNG 格式
png_path = "pinOff.png"
gif.save(png_path, 'PNG')

print(f"GIF 的第一幀已保存為 {png_path}")
