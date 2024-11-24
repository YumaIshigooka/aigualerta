from aigualerta.services.display_handler import user_df_has_been_uploaded, is_process_data_button_pressed, show_results

def load_page():
    if user_df_has_been_uploaded() and is_process_data_button_pressed():
        show_results()