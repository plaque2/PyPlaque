from matplotlib.cbook import boxplot_stats
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm.auto import tqdm
from sklearn.preprocessing import MinMaxScaler

def barplot_quants(abs_df, save_path=None,normalize=False):
    """
    **barplot_quants Function**
    This function generates a bar plot to visualize quantitative data, optionally normalized. It 
    takes a dataframe containing the quantitative data and generates a bar plot using seaborn. 
    The bars can be optionally normalized for better comparison across different types (specified 
    by 'type' column). The function adjusts the width of each bar for better visual presentation 
    and saves the plot if a save path is provided. It also sets specific labels and formatting 
    details to enhance readability and aesthetics.
    
    Args:
        abs_df (pd.DataFrame, required): A dataframe containing quantitative data to be plotted, 
                                        with columns 'Quant' for quantification and optionally 
                                        'Values_scaled' if normalization is enabled.  
        save_path (str or None, optional): The file path where the plot will be saved if provided; 
                                        otherwise, it is displayed interactively. Defaults to None.
        normalize (bool, optional): If set to True, scales the values for better visualization by 
                                    normalizing them using MinMax scaling. Defaults to False.
    
    Returns:
        None: The function generates and optionally saves a matplotlib bar plot based on the 
        arguments provided.
        
    Raises:
        TypeError: If any of the input arguments do not match their expected types as specified 
        in the method signature.
    """
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
    """
    **boxplot_quants Function**
    This function generates a box plot to visualize quantitative measures and provides additional 
    statistics if specified. It takes a dataframe containing the quantitative measures and a 
    specific column name for which the boxplot should be created. It optionally returns the 
    statistical details of the plotted data. The function plots the boxplot using seaborn and 
    annotates it with calculated statistics such as median, mean, lower whisker, upper whisker, 
    etc., rounded to two decimal places. If a save path is provided, the plot will be saved at that 
    location with specified parameters for quality and layout optimization.
    
    Args:
        plq_measures_df (pd.DataFrame, required): A dataframe containing the quantitative measures 
                                                to be plotted.
        col_name (str, required): The name of the column in `plq_measures_df` that contains the data 
                                to plot.
        return_stats (bool, optional): If set to True, returns a dataframe with statistical details 
                                        about the boxplot. Defaults to False.
        save_path (str or None, optional): The file path where the plot will be saved if provided; 
                                        otherwise, it is displayed interactively. Defaults to None.

    Returns:
        pd.DataFrame or None: If `return_stats` is True, returns a dataframe with statistical 
        details of the boxplot. Otherwise, returns None.
        
    Raises:
        TypeError: If any of the input arguments do not match their expected types as specified in 
        the method signature.
    """
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
                          size='small', color='k', weight='semibold', 
                          bbox=dict(facecolor='lightgray'))

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
    """
    **create_grouped_bar_from_df Function**
    This function creates a grouped bar plot from two dataframes based on specified column values.
    It combines viral and control data from two separate dataframes into one dataframe and 
    optionally normalizes the values for better comparison. It then generates a grouped bar plot to 
    visualize the quantitative information across different types (viral vs. control). If 
    `normalize` is set to True, the values are scaled using MinMax scaling for better visual 
    representation. The function optionally saves the generated plot if a save path is provided.
    
    Args:
        abs_df_img (pd.DataFrame, required): A dataframe containing quantitative data specific to 
                                            viral samples.
        abs_df_img_cont (pd.DataFrame, required): A dataframe containing quantitative data specific 
                                                to control samples.
        col_name (str, required): The name of the column in both dataframes that contains the values 
                                to be plotted.
        normalize (bool, optional): If set to True, scales the quantitative values using MinMax 
                                    scaling for better visualization. Defaults to False.
        save_path (str or None, optional): The file path where the plot will be saved if provided; 
                                        otherwise, it is displayed interactively. Defaults to None.
    
    Returns:
        None: The function generates and optionally saves a matplotlib bar plot based on the 
        arguments provided.
        
    Raises:
        TypeError: If any of the input arguments do not match their expected types as specified 
        in the method signature.
    """
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
        combined_df['Values_scaled'] = scaler.fit_transform(
                                        combined_df['Values'].values.reshape(-1,1))
        combined_df.drop(['Values'],axis=1,inplace=True)

    barplot_quants(combined_df,save_path=save_path,normalize=normalize)


def compare_plaque_detection_from_image(i,j,true_count, mask, plaques_list, 
                                        mask_gadjusted, plaques_list_gadjusted,save_path=None):
    """
    **compare_plaque_detection_from_image Function**
    This function compares plaque detection results from two different images (original and 
    gamma-adjusted) by overlaying bounding boxes. It visualizes the detected plaques on top of both 
    the original mask image and a gamma-adjusted version of it using bounding boxes. 
    The visualization includes title labeling with well coordinates (i, j), which are passed as 
    arguments to the function. If a save path is provided via the `save_path` parameter, the plot 
    will be saved at that location using specified parameters for quality and layout optimization.
    
    Args:
        i (int, required): The x-coordinate or row index of the well being visualized.  
        j (int, required): The y-coordinate or column index of the well being visualized.
        true_count (int, required): The expected number of plaques, used for validation and 
                                    comparison purposes.
        mask (object, required): An object representing the original mask from which plaques 
                                were detected. This is typically a numpy array with additional 
                                metadata if applicable.
        plaques_list (list, required): A list of objects containing plaque information including 
                                    bounding box coordinates (`bbox`), detected from the `mask`.
        mask_gadjusted (object, required): An object representing the mask from the gamma-adjusted 
                                        image, similar to `mask`. 
        plaques_list_gadjusted (list, required): A list of objects containing plaque information 
                                                including bounding box coordinates (`bbox`), 
                                                detected from the `mask_gadjusted`.
        save_path (str or None, optional): The file path where the plot will be saved if provided; 
                                    otherwise, it is displayed interactively. Defaults to `None`.
    
    Returns:
        None: The function displays and optionally saves a matplotlib figure based on the arguments 
        provided.
        
    Raises:
        TypeError: If any of the input arguments do not match their expected types as specified in 
        the method signature.
    """
    
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
                            fill=False, edgecolor='red', linewidth=2) 
                            for plq in tqdm(plaques_list_gadjusted)]
    _ = [ax2.add_patch(rect) for rect in tqdm(rect_list)]
    ax2.set_axis_off()
    ax2.set_title(str(i)+","+str(j)+" Gamma Adjusted")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()

    return

def plot_bbox_plaques_mask(i,j,mask,plaques_list,save_path=None):
    """
    **plot_bbox_plaques_mask Function**
    This function plots a masked image of plaques overlaid with bounding boxes and saves it if a 
    save path is provided. It visualizes the plaque masks and draws bounding boxes around each 
    plaque detected in `plaques_list`. The visualization includes title labeling with well 
    coordinates (i, j), which are passed as arguments to the function. If a save path is provided 
    via the `save_path` parameter, the plot will be saved at that location using specified 
    parameters for quality and layout optimization.
    
    Args:
        i (int, required): The x-coordinate or row index of the well being visualized.
        j (int, required): The y-coordinate or column index of the well being visualized.
        mask (np.ndarray, required): A 2D numpy array representing the original mask image, 
                                    typically from nuclei images before plaque segmentation.
        plaques_list (list, required): A list of objects containing plaque information including 
                                    bounding box coordinates (`bbox`, required), which are used to 
                                    draw rectangles on top of the `mask`.
        save_path (str or None, optional): The file path where the plot will be saved if provided;
                                    otherwise, it is displayed interactively. Defaults to `None`.
    
    Returns:
        None: The function displays and optionally saves a matplotlib figure based on the 
        arguments provided.
        
    Raises:
        TypeError: If any of the input arguments do not match their expected types as specified 
        in the method signature.
    """
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