import streamlit
import requests
import pandas
import snowflake.connector

from urllib.error import URLError


def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return fruityvice_normalized

def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
		return my_cur.fetchall()
def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit  + "')")
		return "Thanks for adding " + new_fruit

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()


streamlit.title('My Mom\'s New Healthy Diner')


streamlit.header('Breakfast Menu')


streamlit.text('🥣 Omega 3 & Bueberry Oatmeal')
streamlit.text('🥗 Kale & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


fruits_selected =  streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)



# New Section to display fruityvice api response

streamlit.header("Fruityvice Fruit Advice")


	

try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error("Please select a fruit to get information.")
	else:
		back_from_function = get_fruityvice_data(fruit_choice)
		streamlit.dataframe(back_from_function)

except URLError as e:
	streamlit.error()

streamlit.write('The user entered', fruit_choice)



# take the json version of the response and normalize it

# output it to the screen as table



#streamlit.text(fruityvice_response.json())

#streamlit.stop()

if streamlit.button('Get Fruit Load List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input('What fruit would you like to add?', '')

if streamlit.button('Add a Fruit to the list'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_snowflake(add_my_fruit)
	streamlit.text(back_from_function)

	streamlit.write('Thanks for adding', add_my_fruit)


#streamlit.text("The fruit load list contains:")
streamlit.dataframe(get_fruit_load_list())

