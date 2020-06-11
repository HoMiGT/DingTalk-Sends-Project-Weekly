from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import Color
from reportlab.platypus import Preformatted
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from math import ceil
import fitz

pdfmetrics.registerFont(TTFont('hei', 'msyh.ttc'))


from PIL import Image

DEFAULT_WIDTH = 1280

PAGE_MARGIN = 80
PAGE_BG_COLOR = (0.32,0.47,0.51)

TITLE_BG = 'static/ProjectWeeklyReport.png'
GANTT_BG = 'static/fig_gantt.png'
TABLE_BG = 'static/fig_table.png'

# 圆角的事情先往后放放

def pdf(path ,start_time,end_time):
    
    # 读取文件 以及背景图 生成的gantt图以及生成的table 
    gantt_width,gantt_height= Image.open(GANTT_BG).size
    table_width,table_height= Image.open(TABLE_BG).size
    
    # 设置pdf画布的大小   默认宽是1920   超过1920的  即俩个图最大的宽度 + 外边框(左右图边距均为160)
    bigger_width = max([gantt_width,table_width])
    bigger_width = bigger_width if bigger_width > DEFAULT_WIDTH else DEFAULT_WIDTH
    gantt_height = ceil((bigger_width / gantt_width)*gantt_height) 
    table_height = ceil((bigger_width / table_width)*table_height)

    page_width = bigger_width + 4 * PAGE_MARGIN

    title_image = Image.open(TITLE_BG)
    title_width,title_height = title_image.size
    title_width = page_width
    resize_precent = title_width / 1920 
    title_height = ceil(resize_precent * title_height)
    # print(title_height)
    page_height =  title_height + ( 80 + gantt_height + 80  + 200 ) + (80 + table_height + 80 + 10 + 200)


    c = canvas.Canvas(path,pagesize=(page_width,page_height))
    c.setFillColorRGB(PAGE_BG_COLOR[0], PAGE_BG_COLOR[1], PAGE_BG_COLOR[2])
    # 给画布添加背景色
    c.rect(0,0, width = page_width,height= page_height,stroke=0,fill=1)


    # 从左下角的原点坐标开始画起

    # 设置table区域  背景色为白色
    c.setFillColorRGB(1,1,1)
    c.rect(80,80,width = bigger_width + 2 * 80,height = table_height + 80 + 10 + 200,stroke=0,fill=1)
    # 画出table的图片
    c.drawImage(TABLE_BG,160,160,width=bigger_width,height = table_height,mask=None)
    # 设置分割符号
    c.setFillColorRGB(PAGE_BG_COLOR[0], PAGE_BG_COLOR[1], PAGE_BG_COLOR[2])
    c.rect(150,160+table_height,width = bigger_width + 20,height = 10,stroke=0,fill=1)

    # 设置table 标题
    # 设置字体以及字体大小
    c.setFont('hei',80)   
    c.drawString(150,160+table_height+10+60,'项目周报详情')
    c.setFont('hei',30)
    c.drawString(bigger_width + 20 + 80 + 75 - 505, table_height + 80 + 10 + 200 + 80 - 130 ,f'周报日期：{start_time} ~ {end_time}')


    # 设置gantt图

    # 设置gantt区域  背景色为白色
    c.setFillColorRGB(1,1,1)
    c.rect(80, 80 + table_height + 80 + 10 + 200 + 80,width = bigger_width + 2 * 80,height = gantt_height + 80  + 200,stroke=0,fill = 1 )

    # 画出gantt图的图片
    c.drawImage(GANTT_BG,160, 80 + table_height + 80 + 10 + 200 + 80 + 80,width=bigger_width,height=gantt_height,mask=None)
    # 设置分割符号
    c.setFillColorRGB(PAGE_BG_COLOR[0], PAGE_BG_COLOR[1], PAGE_BG_COLOR[2])
    c.rect(150,80 + table_height + 80 + 10 + 200 + 80 + 80 +gantt_height ,width = bigger_width + 20,height = 10,stroke=0,fill=1)
    # gantt图图片
    c.setFont('hei',80)   
    c.drawString(150,80 + table_height + 80 + 10 + 200 + 80 + gantt_height  + 80 + 80,'项目进度图')

    # 设置title 
    c.drawImage(TITLE_BG,0,80 + table_height + 80 + 10 + 200 + 80 + gantt_height + 80  + 200 ,width=title_width,height=title_height)

    # 绘制时间
    
    # 获取默认样式的字典对象
    styleSheet = getSampleStyleSheet()
    # 获取文本的样式
    style = styleSheet['BodyText']
    # 设置字体
    style.fontName = 'hei'   # 字体
    # 设置字体大小
    style.fontSize = ceil(resize_precent * 60 )  # 字体大小
    # 设置行间距
    style.leading =  ceil(resize_precent * 70 )
    # 设置字体颜色
    style.textColor = PAGE_BG_COLOR 
    # 官方文档提示 中文要有该参数
    style.wordWrap = 'CJK'    
    # 文本格式化
    text = f'''
    {start_time}
    /
    {end_time}
    '''
    p =Preformatted(text,style, newLineChars='')
    # 指定文本区域大小
    p.wrapOn(c,321, 224)
    # 绘画在画布上
    time_position_x = ceil(1400/1920*page_width)
    time_position_y = ceil(129/482*title_height) + ( 80 + gantt_height + 80  + 200 ) + (80 + table_height + 80 + 10 + 200)
    p.drawOn(c, time_position_x, time_position_y)

    c.showPage()
    c.save()
    



 
def pyMuPDF_fitz(path = 'static/pws.pdf',start_time='2020.06.01',end_time='2020.06.07'):
    pdf(path,start_time,end_time)
    pdfDoc = fitz.open(path)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        pix.writePNG('static/pws.png')
        

if __name__ == "__main__":
    # pdf()

    pyMuPDF_fitz()




 

