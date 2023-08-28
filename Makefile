# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit:
	-@streamlit run app.py


# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------
install:
	@pip install . -U


data:

	@data_update.py