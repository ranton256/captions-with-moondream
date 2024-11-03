import streamlit as st
from PIL import Image
from caption import process_image, load_model
from collections import namedtuple

CaptionModel = namedtuple('ModelConfig', ['model', 'tokenizer'])


@st.cache_resource
def get_model():
    model, tokenizer = load_model()
    return CaptionModel(model, tokenizer)


def main():
    st.set_page_config(
        page_title="Image Caption Generator",
        page_icon="🖼️",
        layout="centered"
    )

    st.sidebar.markdown("""
        ### Connect
        - My Website: [ranton.org](https://ranton.org)
        - Follow me on [LinkedIn](https://linkedin.com/in/ranton)
        """)

    st.title("Image Caption Generator 🖼️")

    st.markdown("View the readme for this app on [GitHub]("
                "https://github.com/ranton256/captions-with-moondream) for documentation and code "
                "including command line and notebook versions.")
    st.subheader("Upload an image and get an AI-generated caption!")

    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['png', 'jpg', 'jpeg'],
        help="Supported formats: PNG, JPG, JPEG"
    )

    if 'caption' not in st.session_state:
        st.session_state.caption = None

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)

            st.image(image, caption="Uploaded Image", use_column_width=True)

            if st.button("Generate Caption"):
                with st.spinner('Generating caption...'):
                    try:
                        caption_model = get_model()
                        caption = process_image(caption_model.model, caption_model.tokenizer, image=image)
                        st.session_state.caption = caption
                    except Exception as e:
                        st.error(f"Error generating caption: {str(e)}")
                        return

            if st.session_state.caption:
                st.success("Caption generated successfully!")
                st.markdown("### Generated Caption")
                st.write(st.session_state.caption)

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return

    # Add information about supported formats
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    This app generates image captions using the Moondream vision model from [M87 Labs](https://www.moondream.ai/)
    which is small enough at 1.87B parameters to run locally and is available under the Apache 2 license.
    You can also find more information about the model on
    🤗 Hugging Face at <https://huggingface.co/vikhyatk/moondream2>.

    The [Transformers](https://github.com/huggingface/transformers) library is used to run the pretrained model
    and the [Pillow](https://python-pillow.org/) is used for handling images.
    
    **Note:** This app is for demonstration purposes only and is not intended for production use.
    
    **Supported formats:**
    - PNG
    - JPG/JPEG
    """)


if __name__ == "__main__":
    main()
