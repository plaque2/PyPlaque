from matplotlib.cbook import boxplot_stats
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm.auto import tqdm
from sklearn.preprocessing import MinMaxScaler

def barplot_quants(abs_df, save_path=None,normalize=False):
    sns.set(font_scale=1.5)
    sns.set_style("ticks")

    _, ax =plt.subplots(1,1,figsize=(5,7))
    plot = sns.barplot(
        x="Quant",
        y= "Values_scaled" if normalize else "Values",
        data=abs_df,
        hue="type",
        errorbar="sd",
        capsize=.2,
        color='black',edgecolor='black',ax=ax
    )
    for bar in plot.patches:
        bar.set_zorder(3)
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - 0.35

        # we change the bar width
        patch.set_width(0.35)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)
        
    plot.set(xlabel=None, xticklabels=[], ylabel=list(abs_df['Quant'])[0])
    plot.tick_params(bottom=False)
    ax.set_ylim([0, np.max(abs_df['Values_scaled' if normalize else 'Values'])])
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.tight_layout()
    plt.show()
    return

def boxplot_quants(plq_measures_df, col_name,return_stats = False,save_path=None):

    # extract relevant column
    plq_measures_df = plq_measures_df[col_name]

    # extract the boxplot stats
    plq_measures_df_stats = [boxplot_stats(plq_measures_df.dropna().values)[0]] 
    # create a dataframe for the stats
    stats = pd.DataFrame(plq_measures_df_stats).iloc[:, [4, 5, 7, 8, 9]].round(2)
    # plot
    _, ax = plt.subplots(figsize=(2, 5))
    box_plot = sns.boxplot(data=plq_measures_df, ax=ax)

    # annotate
    for xtick in box_plot.get_xticks():
        for col in stats.columns:
            box_plot.text(xtick, stats[col][xtick], stats[col][xtick], horizontalalignment='left', 
                          size='small', color='k', weight='semibold', bbox=dict(facecolor='lightgray'))

    plt.title(col_name)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()

    if return_stats:
        return stats
    else:
        return

def create_grouped_bar_from_df(abs_df_img,abs_df_img_cont,col_name,normalize=False,save_path=None):
    iter_ = len(abs_df_img)
    abs_iter_ls  = np.array(list(abs_df_img[col_name])).flatten()
    abs_df = pd.DataFrame({
            "Values": abs_iter_ls,
            "Quant": np.array([col_name]*iter_).flatten()
        })
    abs_df['type'] = 'viral'
    
    iter_ = len(abs_df_img_cont)
    abs_iter_ls  = np.array(list(abs_df_img_cont[col_name])).flatten()
    abs_df_cont = pd.DataFrame({
            "Values": abs_iter_ls,
            "Quant": np.array([col_name]*iter_).flatten()
        })
    abs_df_cont['type'] = 'control'

    combined_df = pd.concat([abs_df,abs_df_cont])

    if normalize:
        scaler = MinMaxScaler()
        combined_df['Values_scaled'] = scaler.fit_transform(combined_df['Values'].values.reshape(-1,1))
        combined_df.drop(['Values'],axis=1,inplace=True)

    barplot_quants(combined_df,save_path=save_path,normalize=normalize)


def compare_plaque_detection_from_image(i,j,true_count, mask, plaques_list, 
                                        mask_gadjusted, plaques_list_gadjusted,save_path=None):
    
    print(mask.name," true count : ", true_count)
    print(mask.name," : ", len(plaques_list))
    print(mask_gadjusted.name," gamma adjusted : ", len(plaques_list_gadjusted))

    _, (ax1, ax2) = plt.subplots(1, 2,figsize=(32,8))
    ax1.imshow(mask.plaques_mask,cmap='gray')
    rect_list = [mpatches.Rectangle((plq.bbox[1], plq.bbox[0]), plq.bbox[3] - plq.bbox[1], 
                                    plq.bbox[2] - plq.bbox[0],
                            fill=False, edgecolor='red', linewidth=2) for plq in tqdm(plaques_list)]
    _ = [ax1.add_patch(rect) for rect in tqdm(rect_list)]
    ax1.set_axis_off()
    ax1.set_title(str(i)+","+str(j))

    ax2.imshow(mask_gadjusted.plaques_mask,cmap='gray')
    rect_list = [mpatches.Rectangle((plq.bbox[1], plq.bbox[0]), plq.bbox[3] - plq.bbox[1], 
                                    plq.bbox[2] - plq.bbox[0],
                            fill=False, edgecolor='red', linewidth=2) for plq in tqdm(plaques_list_gadjusted)]
    _ = [ax2.add_patch(rect) for rect in tqdm(rect_list)]
    ax2.set_axis_off()
    ax2.set_title(str(i)+","+str(j)+" Gamma Adjusted")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()

    return

def plot_bbox_plaques_mask(i,j,mask,plaques_list,save_path=None):
    _, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(mask,cmap='gray')
    rect_list = [mpatches.Rectangle((plq.bbox[1], plq.bbox[0]), plq.bbox[3] - plq.bbox[1], 
                                plq.bbox[2] - plq.bbox[0],
                        fill=False, edgecolor='red', linewidth=2) for plq in tqdm(plaques_list)]
    _ = [ax.add_patch(rect) for rect in tqdm(rect_list)]
    ax.set_axis_off()
    plt.title(str(i)+","+str(j))
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()

    return