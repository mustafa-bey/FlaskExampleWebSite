import pyautogui
import time

time.sleep(4)
pyautogui.write("app.route('/movies', methods=['GET', 'POST'])")
time.sleep(3)
pyautogui.press('enter')
time.sleep(2)
pyautogui.write('def movies_page():')
time.sleep(3)
pyautogui.press('enter')
time.sleep(2)
pyautogui.write('if request.method == "GET":')
pyautogui.press('enter')
time.sleep(2)
pyautogui.write('movies = select("id, name, likes, dislikes, image", "movie", asDict=True)')
time.sleep(2)
pyautogui.press('enter')
time.sleep(2)
pyautogui.write('return render_template("movies.html", movies=movies)')

