import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rectpack import *
import pandas as pd
import warnings
import time
import math
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as img
import datetime
import pytz
import json
import os
warnings.filterwarnings('ignore')


t0 = time.time()
os.chdir(os.path.dirname(__file__))

def input_data(input_file, options):
    init_bins=[]
    file = input_file
    with open("../teal/templates/static/impdatajson.json") as f:
        data = json.load(f)
    for item in data:
        if item['Truck_Name'] in [opt[0] for opt in options]:
            index = next(i for i, opt in enumerate(options) if opt[0] == item['Truck_Name'])
            l = item['Length']
            b = item['Breadth']
            v = options[index][1]
            truck_des = (l, b, v)
            # print(truck_des)
            init_bins.append(truck_des)
            # print(init_bins)
    remaining1,nos1,no_of_pallets1=execution(file, init_bins)
    return remaining1,nos1,no_of_pallets1

def generate_colors(count):
    if count <= 0:
        return []
    colors = set()
    while len(colors) < count:
        color = (random.random(), random.random(), random.random())
        if color not in colors:
            colors.add(color)
    return list(colors)


def create_rect(x, y, w, h, color):
    rect = matplotlib.patches.Rectangle((x, y), w, h, color=color)
    return rect


def plotter(all_rect):
    lis = set([i[0] for i in all_rect])
    #     print([i[0] for i in all_rects],set([i[0] for i in all_rect]))
    bin_dict0 = {i[1]: i[0] for i in list(enumerate(lis))}
    max_ = len(bin_dict0)
    plots_per_page=3
    no_of_pages=math.ceil(max_/plots_per_page)
    #     print(bin_dict0)
    pp = PdfPages(r"../teal/templates/static/res.pdf")
    input_image=img.imread(r"../teal/templates/static/logo1.png")
    desired_timezone = pytz.timezone('Asia/Kolkata')
    for page in range(no_of_pages):
      fig, ax = plt.subplots(plots_per_page, 1, figsize=(8.3, 11.7))
      #     print("Number of axes created:",str(max_+1))
      all_axes = fig.get_axes()
      #     print("all_axes:",all_axes)
      colors = generate_colors(len(all_rect))

      for i in range(plots_per_page):
            bin_idx = page * plots_per_page + i
            if(bin_idx >= max_):
                all_axes[i].axis('off')
                continue
            all_axes[i].set_xlim([0, bin_id_dict[list(bin_dict0.keys())[bin_idx]][0]])
            all_axes[i].set_ylim([0, bin_id_dict[list(bin_dict0.keys())[bin_idx]][1]])
            l_truck = str(all_axes[i].get_xlim()[-1])
            b_truck = str(all_axes[i].get_ylim()[-1])

            all_axes[i].set_title(
                'Truck ' + str(bin_dict0[list(bin_dict0.keys())[bin_idx]]+1) + ":" +
                l_truck + 'x' + b_truck + " (inches)",
                ha='right'
            )
      for i in range(len(all_rect)):
            b, x, y, w, h, r = all_rect[i]
            rect = create_rect(x, y, w, h, colors[i])
            bin_idx = list(bin_dict0.keys()).index(b)
            page_idx = bin_idx // plots_per_page
            subplot_idx = bin_idx % plots_per_page
            if page_idx == page:
                all_axes[subplot_idx].add_patch(rect)
                rx, ry = rect.get_xy()
                cx = rx + rect.get_width() / 2.0
                cy = ry + rect.get_height() / 2.0
                all_axes[subplot_idx].annotate(list(rect_details.values())[r][0], (cx, cy),
                    color='white', weight='bold', fontsize=10, ha='center', va='center'
                )
      if page==0:
        fig.suptitle("Matplotlib",y=0.9375,fontsize=20,fontweight='bold')
        fig.text(0.04,0.97,"Created on "+str(datetime.datetime.now(desired_timezone)))

      logo=fig.add_axes([0.845,0.895,0.1,0.1],anchor="NE",zorder=1)
      logo.imshow(input_image)
      logo.axis("off")

      pp.savefig(fig)
      plt.close(fig)

    pp.close()
    plt.close('all')
    return max_


bin_id_dict = {}


def main(rects, bins):
    packer = newPacker(bin_algo=PackingBin.BBF, sort_algo=SORT_LSIDE, pack_algo=GuillotineBssfSas, rotation=True) #'Enable'
    for r in rects:
        packer.add_rect(r[0], r[1], rid=r[2])
    for b in range(len(bins)):
        packer.add_bin(*bins[b], bid=b)
        bin_id_dict[b] = bins[b]
    packer.pack()

    all_rects = []
    for abin in packer:
        for r in abin:
            all_rects.append((abin.bid, r.x, r.y, r.width, r.height, r.rid))
    print(all_rects)
    lis = plotter(all_rects)

    return all_rects, lis
#     return all_rects


def execution(file,init_bins):
    bins = [(i[0],i[1]) for i in init_bins for j in range(i[2])]
    #-------------------------------------------------------------
    #19*7.5,32*8,40*8,21*8
    #19*7.5 - (228,90)
    #32*8 - (384,96)
    #40*8 - (480,96)
    #21*8 - (252,96)
    #-------------------------------------------------------------
    raw_df = pd.read_excel(file)
    df = raw_df.drop([raw_df.index[i] for i in range(0,6)])

    df = df.drop([raw_df.index[-1] ])
    no_of_pallets=len(df)
    df.columns = ['SL.NO.','MACHINE DESCRIPTION','ID_LENGTH_IN','ID_WIDTH_IN','ID_HEIGHT_IN',
                'OD_LENGTH_IN','OD_WIDTH_IN','OD_HEIGHT_IN',
                'OD_LENGTH_FT','OD_WIDTH_FT','OD_HEIGHT_FT',
                'QTY','C.NO','Packing Type','REMARKS']
    df = df.reset_index()
    rel_df =df[['SL.NO.','MACHINE DESCRIPTION','OD_LENGTH_IN','OD_WIDTH_IN','OD_HEIGHT_IN','QTY']]
    rel_df['index'] = rel_df.index
    rects = list()
    global rect_details
    rect_details= dict()
    for _,row in rel_df.iterrows():
        rects.append((row['OD_LENGTH_IN'],row['OD_WIDTH_IN'],row['index']))
        rect_details[row['index']]=[row['SL.NO.'], row['OD_LENGTH_IN'],row['OD_WIDTH_IN'] ]
    rect_details_org = rect_details.copy()
    #-------------------------------------------------------------
    packed_rect,nos = main(rects,bins)
    #-------------------------------------------------------------
    packed_rect_ids = list()
    for i in packed_rect:
        packed_rect_ids.append(i[-1])
    remaining=0
    if len(packed_rect_ids)!= len(range(rects[0][-1],rects[-1][-1]))+1:
        remaining=(len(range(rects[0][-1],rects[-1][-1]))+1)-len(packed_rect_ids)
        print('BINS NOT SUFFICIENT',remaining,'BOX/BOXES YET TO BE PACKED')
        print('Total bins used so far:',nos)
        print('unpacked bins:')
        for ids in packed_rect_ids:
            rect_details.pop(ids)
        print('SNO.','--','Dim')
        for i in rect_details.items():
            print(i[0],',',i[1][1],'x',i[1][2])
    else:
        print('Total bins used so far:',nos)
    print(rect_details)
    print(bin_id_dict)
    t1 = time.time() - t0
    # print("Program execution time: ", (t0 - t1)/60000)
    return remaining,nos,no_of_pallets


