import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import av
import os
import subprocess
import sys

def convert_avif_to_png(input_path, output_folder):
    # AVIF 파일을 읽기
    container = av.open(input_path)
    for frame in container.decode(video=0):
        avif_image = frame.to_image()
        break  # 첫 번째 프레임만 사용

    # 이미지를 Pillow 형식으로 변환
    image = avif_image.convert("RGBA")
    
    # 저장할 경로 지정
    filename = os.path.basename(input_path)
    output_filename = os.path.splitext(filename)[0] + ".png"
    output_path = os.path.join(output_folder, output_filename)
    
    # PNG로 저장
    image.save(output_path, "PNG")
    print(f"{filename}를 {output_filename}로 변환하였습니다.")
    return output_filename

def select_files_and_convert():
    # 파일 선택 안내 메시지
    messagebox.showinfo("파일 선택", "변환할 파일을 선택해 주십시오")
    
    # 파일 탐색기 열기 (여러 파일 선택 가능)
    input_paths = filedialog.askopenfilenames(filetypes=[("AVIF files", "*.avif")])
    if not input_paths:
        print("파일을 선택하지 않았습니다.")
        return

    # 실행 파일의 경로 확인
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    # output 폴더 생성
    output_folder = os.path.join(base_path, "output")
    os.makedirs(output_folder, exist_ok=True)

    # 선택된 파일들을 변환하고, 변환된 파일들의 리스트를 저장
    converted_files = []
    for input_path in input_paths:
        converted_files.append(convert_avif_to_png(input_path, output_folder))

    total_files = len(converted_files)
    print(f"총 {total_files}개의 파일이 변환 완료되었습니다.")

    # 변환 완료 메시지 박스
    messagebox.showinfo("완료", f"총 {total_files}개의 파일이 변환 완료되었습니다.")

    # 저장된 폴더 열기
    open_folder = messagebox.askyesno("폴더 열기", "저장된 폴더를 열까요?")
    if open_folder:
        subprocess.Popen(f'explorer "{output_folder}"')

# tkinter 루트 생성
root = tk.Tk()
root.withdraw()  # 루트 창 숨기기

# 파일 선택 및 변환 실행
select_files_and_convert()
