# Letterboxd-diary-collage-maker
Script that creates a collage of movies watched on a chosen month based on your Letterboxd username. The script does not require your account password, nor access to Letterboxd's API.

When running the script, enter the Letterboxd username, the year and the month as a two character number (e.g. 09 for September).

If you enjoyed this script, follow me on [Letterboxd](https://letterboxd.com/NeroKnox/)!

Example of image generated (username='neroknox',year='2023',month='09'):
![Movies_2023_09](https://github.com/NeroKnox/Letterboxd-diary-collage-maker/assets/88953659/76248596-8eb3-4081-b5af-4b7c2e0254ba)

Required libraries: 'selenium' and 'PIL'.

You also need to install the WebDriver for Google Chrome. Depending on your Chrome version, the correct driver may be found [here](https://chromedriver.chromium.org/downloads) or [here](https://googlechromelabs.github.io/chrome-for-testing/). After downloading it, you need add the path to the driver file in the code before running it.
