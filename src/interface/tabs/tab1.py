import streamlit as st
import utils
import utils_plot


def load_page():

    # Upload data if not already done
    if st.session_state.user_df is None:
        st.session_state.user_df = utils.upload_data()

    if st.session_state.user_df is not None:
        st.subheader("Uploaded Dataset")
        st.write(st.session_state.user_df.head())

        # Process setup_data if not already done
        if st.session_state.user_df_setup is None:
            st.session_state.user_df_setup = utils.setup_data(st.session_state.user_df)

        if st.session_state.user_df_setup is not None:
            st.subheader("Processed Dataset")
            st.write(st.session_state.user_df_setup.head())

            # Process setup_input if not already done
            if st.session_state.user_df_input is None:
                st.session_state.user_df_input = utils.setup_input(st.session_state.user_df_setup)

            if st.session_state.user_df_input is not None:
                st.subheader("Input that will be used")
                st.write(st.session_state.user_df_input.head())

                # Handle prediction
                if st.button("Predict"):
                    st.session_state.user_df_predicted = utils.predict(st.session_state.user_df_input)

                # Show predictions if available
                if st.session_state.user_df_predicted is not None:
                    st.subheader("Prediction Results")
                    st.write(st.session_state.user_df_predicted[st.session_state.user_df_predicted["LEAK"] == True].head())
                    utils_plot.plot_durations(st.session_state.user_df_predicted)
    else:
        st.write("If you are willing to **load your dataset from the data folder**, please refer to the *data from folder* tab.")