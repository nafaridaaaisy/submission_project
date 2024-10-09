# DASHBOARD

# mengimpor library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')



# mendefinisikan fungsi cheatsheet
# Fungsi Penjualan Produk berdasarkan Kategori
def create_total_orders_df(all_data_df):
    total_orders_df = all_data_df.groupby("product_category_name_english").order_id.sum().sort_values(ascending=False).reset_index()
    return total_orders_df
# Fungsi Customer berdasarkan City
def create_customerbycity_df(all_data_df):
    customerbycity_df = all_data_df.groupby(by="customer_city").customer_id.nunique().reset_index()
    customerbycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return customerbycity_df
# Fungsi Customer berdasarkan State
def create_customerbystate_df(all_data_df):
    customerbystate_df = all_data_df.groupby(by="customer_state").customer_id.nunique().reset_index()
    customerbystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return customerbystate_df
# Fungsi Seller berdasarkan City
def create_sellerbycity_df(all_data_df):
    sellerbycity_df = all_data_df.groupby(by="seller_city").seller_id_x.nunique().reset_index()
    sellerbycity_df.rename(columns={
        "seller_id_x": "seller_count"
    }, inplace=True)
    
    return sellerbycity_df
# Fungsi Seller berdasarkan State
def create_sellerbystate_df(all_data_df):
    sellerbystate_df = all_data_df.groupby(by="seller_state").seller_id_x.nunique().reset_index()
    sellerbystate_df.rename(columns={
        "seller_id_x": "seller_count"
    }, inplace=True)
    
    return sellerbystate_df



# load berkas all_data_df
all_data_df = pd.read_csv("https://raw.githubusercontent.com/nafaridaaaisy/submission_project/refs/heads/master/dashboard/all_data_df.csv")



# mengurutkan dataframe berdasarkan order_purchase_timestamp
datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_data_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_data_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data_df[column] = pd.to_datetime(all_data_df[column])



# membuat filter dengan widget date_input
min_date = all_data_df["order_purchase_timestamp"].min()
max_date = all_data_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan judul
    st.header('Brazilian E-Commerce Analysis: Products and Demography')
    # Menambahkan foto
    st.image("https://th.bing.com/th/id/OIP.6BxAHx8wrRNtCng9FPaThwHaFU?rs=1&pid=ImgDetMain")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Choose Time', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # Menambahkan caption
    st.markdown("""
    **The main goals for this analysis are:**

    1. Deciding the best and least seller product based on its categories. This analysis might be useful for related industries to create strategy to innovate their products.
    
    2. Analyze the demography of both customers and sales. It might be useful for related industries to conduct some strategies of sales by identifying the most promising area.
    
    *The analysis conducted here uses open-source data available from the source: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce.*
    """
    )



#filtering data dari all_data_df
main_df = all_data_df[(all_data_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_data_df["order_purchase_timestamp"] <= str(end_date))]



#memanggil dataframe
total_orders_df = create_total_orders_df(all_data_df)
customerbycity_df = create_customerbycity_df(all_data_df)
customerbystate_df = create_customerbystate_df(all_data_df)
sellerbycity_df = create_sellerbycity_df(all_data_df)
sellerbystate_df = create_sellerbystate_df(all_data_df)



# VISUALISASI DATA
# Mengatur layout kolom
# Mengatur layout kolom
col1, col2 = st.columns([1, 3])  # Proporsi kolom: 3 untuk teks, 1 untuk gambar
with col1:
    # Menambahkan custom HTML untuk mengatur tinggi gambar
    st.markdown(
        """
        <style>
        .resized-image {
            display: flex;
            align-items: bottom;       /* Memusatkan secara vertikal */
            width: 300px;
            height: 3000px;  /* Atur tinggi sesuai kebutuhan */
            object-fit: cover;  /* Menjaga proporsi tanpa distorsi */
        }
        </style>
        <img src="https://th.bing.com/th/id/OIP.CyT_tkAH01Dp7TY4nLnvJgHaHa?rs=1&pid=ImgDetMain">
        """,
        unsafe_allow_html=True
    )
with col2:
    # Menggunakan CSS untuk menambahkan margin pada title agar vertikal center dengan gambar
    st.markdown(
        """
        <style>
        .left-aligned-title {
            display: flex;
            align-items: center;       /* Memusatkan secara vertikal */
            height: 100px;  /* Sesuaikan tinggi sesuai kebutuhan */
            margin-top: 100px;  /* Sesuaikan angka ini agar sesuai dengan gambar */
            text-align: left;  /* Mengatur teks agar berada di kiri */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h1 class="centered-title">Brazilian E-Commerce: An Insight of Product Sales and Demographic Trends</h1>', unsafe_allow_html=True)


# Best & Worst Performing Product
with st.expander("Product Sales Performance", expanded=True):  # Set expanded=True untuk menampilkan konten secara default
    st.caption("This section contains information related to product categories with the highest and lowest sales purchased by customers.")
    # Header untuk grafik
    st.header("Product Sales")
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 20))
    colors = ["#228C22"] * 3 + ["#D3D3D3"] * 9 # Warna untuk kategori terbaik dan terburuk
    # Best product (top 10)
    sns.barplot(x="total_orders", y="product_category_name_english", data=all_data_df.sort_values(by="total_orders", ascending=False).head(103608), hue="product_category_name_english", palette=colors, ax=ax[0], legend=False)
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
    ax[0].tick_params(axis ='y', labelsize=33)
    ax[0].tick_params(axis ='x', labelsize=30)
    # Worst product (top 10)
    sns.barplot(x="total_orders", y="product_category_name_english", data=all_data_df.sort_values(by="total_orders", ascending=True).head(292), hue="product_category_name_english", palette=colors, ax=ax[1], legend=False)
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()                        # Membalik sumbu x untuk grafik terburuk
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=33)
    ax[1].tick_params(axis ='x', labelsize=30)
    plt.suptitle("Best and Worst Performing Product based on Category by Number of Sales", fontsize=75, fontweight='bold')
    plt.show()
    st.pyplot(fig)



# Visualisasi Data Customer by City
# Import library
import seaborn as sns
import matplotlib.pyplot as plt
with st.expander("Customer Demography", expanded=True):  # Set expanded=True untuk menampilkan konten secara default
    st.caption("This section contains information related to the distribution of customers based on city and state.")
    st.header("Customer by City")
    # Mengelompokkan data berdasarkan kota dan menghitung jumlah unik customer_id
    customerbycity_df = all_data_df.groupby(by="customer_city").customer_id.nunique().reset_index()   # group by customer city and count unique customer IDs
    customerbycity_df.rename(columns={"customer_id": "customer_count"}, inplace=True)                         # rename the column for clarity
    customerbycity_df_sorted = customerbycity_df.sort_values(by="customer_count", ascending=False)                    # sort by customer count in descending order
    # Membuat bar plot
    plt.figure(figsize=(12, 6))  # Ubah ukuran plot agar sesuai di Streamlit
    colors_ = ["#228C22"] * 3 + ["#D3D3D3"] * 7  # Warna untuk bar
    sns.barplot(
        x="customer_count",
        y="customer_city",
        data=customerbycity_df_sorted.head(10),
        hue="customer_city",
        palette=colors_,
        legend=False
    )
    # Mengatur judul dan label
    plt.title("Number of Customer by City", loc="center", fontsize=25, fontweight='bold')
    plt.xlabel("Customer Count", fontsize=18)
    plt.ylabel("Customer City", fontsize=18)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=11)
    # Menampilkan plot di Streamlit
    st.pyplot(plt)



    # Visualisasi Data Customer by State
    # Import library
    import seaborn as sns
    import matplotlib.pyplot as plt
    st.header("Customer by State")
    # Mengelompokkan data berdasarkan state dan menghitung jumlah unik customer_id
    customerbystate_df = all_data_df.groupby(by="customer_state").customer_id.nunique().reset_index()   # group by customer state and count unique customer IDs
    customerbystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)                         # rename the column for clarity
    customerbystate_df_sorted = customerbystate_df.sort_values(by="customer_count", ascending=False)                    # sort by customer count in descending order
    # Membuat bar plot
    plt.figure(figsize=(12, 6))  # Ubah ukuran plot agar sesuai di Streamlit
    colors_ = ["#228C22"] * 3 + ["#D3D3D3"] * 7  # Warna untuk bar
    sns.barplot(
        x="customer_count",
        y="customer_state",
        data=customerbystate_df_sorted.head(10),
        hue="customer_state",
        palette=colors_,
        legend=False
    )
    # Mengatur judul dan label
    plt.title("Number of Customer by State", loc="center", fontsize=25, fontweight='bold')
    plt.xlabel("Customer Count", fontsize=18)
    plt.ylabel("Customer State", fontsize=18)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=11)
    # Menampilkan plot di Streamlit
    st.pyplot(plt)


# Visualisasi Data Seller by City
# Import library
import seaborn as sns
import matplotlib.pyplot as plt
with st.expander("Seller Demography", expanded=True):  # Set expanded=True untuk menampilkan konten secara default
    st.caption("This section contains information related to the distribution of sellers based on city and state.")
    st.header("Seller by City")
    # Mengelompokkan data berdasarkan kota dan menghitung jumlah unik seller_id_x
    sellerbycity_df = all_data_df.groupby(by="seller_city").seller_id_x.nunique().reset_index()   # group by seller city and count unique seller IDs
    sellerbycity_df.rename(columns={"seller_id_x": "seller_count"}, inplace=True)                         # rename the column for clarity
    sellerbycity_df_sorted = sellerbycity_df.sort_values(by="seller_count", ascending=False)                    # sort by seller count in descending order
    # Membuat bar plot
    plt.figure(figsize=(12, 6))  # Ubah ukuran plot agar sesuai di Streamlit
    colors_ = ["#228C22"] * 3 + ["#D3D3D3"] * 7  # Warna untuk bar
    sns.barplot(
        x="seller_count",
        y="seller_city",
        data=sellerbycity_df_sorted.head(10),
        hue="seller_city",
        palette=colors_,
        legend=False
    )
    # Mengatur judul dan label
    plt.title("Number of Seller by City", loc="center", fontsize=25, fontweight='bold')
    plt.xlabel("Seller Count", fontsize=18)
    plt.ylabel("Seller City", fontsize=18)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=11)
    # Menampilkan plot di Streamlit
    st.pyplot(plt)



    # Visualisasi Data Seller by State
    # Import library
    import seaborn as sns
    import matplotlib.pyplot as plt
    st.header("Seller by State")
    # Mengelompokkan data berdasarkan kota dan menghitung jumlah unik seller_id_x
    sellerbystate_df = all_data_df.groupby(by="seller_state").seller_id_x.nunique().reset_index()   # group by seller state and count unique seller IDs
    sellerbystate_df.rename(columns={"seller_id_x": "seller_count"}, inplace=True)                         # rename the column for clarity
    sellerbystate_df_sorted = sellerbystate_df.sort_values(by="seller_count", ascending=False)                    # sort by seller count in descending order
    # Membuat bar plot
    plt.figure(figsize=(12, 6))  # Ubah ukuran plot agar sesuai di Streamlit
    colors_ = ["#228C22"] * 3 + ["#D3D3D3"] * 7  # Warna untuk bar
    sns.barplot(
        x="seller_count",
        y="seller_state",
        data=sellerbystate_df_sorted.head(10),
        hue="seller_state",
        palette=colors_,
        legend=False
    )
    # Mengatur judul dan label
    plt.title("Number of Seller by state", loc="center", fontsize=25, fontweight='bold')
    plt.xlabel("Seller Count", fontsize=18)
    plt.ylabel("Seller state", fontsize=18)
    plt.tick_params(axis='y', labelsize=12)
    plt.tick_params(axis='x', labelsize=11)
    # Menampilkan plot di Streamlit
    st.pyplot(plt)
