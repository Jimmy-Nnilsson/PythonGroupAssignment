# PythonGroupAssignment
# Group 2
ML interaction

### Uppfyllda kriterier
- Det ska levereras i ett GitHub repository
  - Det ska finnas en tydlig README för hur man startar appen lokalt på sin dator
  - Detta innebär att filer som t ex requirements.txt är självklara
- Användaren ska kunna ladda upp egen data i appen
  - Den datan ska sedan sparas i databasen så att användaren kan gå tillbaka och välja samma data igen, utan att behöva ladda upp den igen
- Appen ska interagera med minst en maskininlärningsmodell via ett API
- Ni ska använda biblioteket Streamlit för att sätta upp en sida som användaren kan interagera via
- Ni ska använda docstrings, clean coding och i mån av behov även kommentarer i koden – kom ihåg att en annan grupp ska kunna förstå koden!
- Tips: innan ni lämnar in ert repo, klona ner det i en ny mapp, gör en helt ny conda environment och följ era egna instruktioner - se till att det går att köra!!

## Start instructions
- Short version: streamlit run main.py
- Press "Start ML Model Server"
  - starts ./src/main.py
  - **Make sure to stop the model server before closing the browser as the application looses the process id when closed**
  - If closed by mistake in a windows 10 machine:
    - Close all python related resources as vscode, pycharm etc.
    - Open "Task Manager" hotkey: (ctrl + shift + escape)
    - Find python in the background processes
    - Mark python
    - Press End Task
- Choose function from the selectbox

### Download repository
**Option 1.** By either visiting https://github.com/Jimmy-Nnilsson/PythonGroupAssignment
 Download the repository by pressing green button code. A dropdown list will appear where you have the choice to download the repo as a zip.

**Option 2.** Go to a folder of choice and open a terminal that can access git.
Write "git clone https://github.com/Jimmy-Nnilsson/PythonGroupAssignment.git"

### Extractingt the repository
**Only for option 1.**
As the repository is compressed it needs to get extracted. Go to the folder where the file was downloaded to.
The default filename should be PythonAssignment01-master.zip. Rightclick the file (for windows 7 and later).
Choose extract all. A window will open and ask for a location to extract the archive to.
As an example we will use *C:\*
Which will put it in C:\PythonAssignment02-master

### Installing the needed software
Install conda by downloading a package from https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation

### Create a conda environment
If conda is installed with the environment path variables then it should work with only printing.
Else open the Anaconda navigator and open a terminal from there. 

Print "*conda create --name pythonenv python=3.9*"

### Activate the environment
Print "*conda activate pythonenv*"

### Update environment with needed packages
Browse to the git repo folder with the terminal.
print "pip install -r requirements.txt"

### Start the python script
- Browse to the location of the files.
- Then type "streamlit run main.py"
When the script is started the default browser will open at localhost:8501 if it doesn't.
Open your preferred browser and browse to "localhost:8501" .

### Script function
The webpages is basicly divided in to two areas. 
## Sidebar
- On the left is a grey area called sidebar.
  - If its hidden there is a small arrow in the top left corner pointing right. Press it to reveal the sidebar.
- Button "Start ML Model Server" Remotely starts the machine learning model server thats provided by nordaxon.
- Button "Stop ML Model Server" Remotely stops the machine learning model server thats provided by nordaxon.
- Text "PID (default 0)" indicates what process id the ml server has on the local computer
- Selectbox "Select ML Model" chooses what model to display at the **Main Page**
## Main Page
### Image Classifier
- Expander "Image Classes"
  - Default classes are: cat, dog, banana
  - Opened and closed with the + or - in its right side area
  - By filling the fields and pressing submit classes the pictures will get classified to the closest matching class.
- Image
  - Drop an image in the area to upload it to the process
- Button "Classify Image" starts either to user provided or default classes
- Button "Update Log" shows the database entries for the current model.
- Input field "Input Id to classify" chooses what picture to classify again
- Button "Classify Table" classifies the picture connected to the chosen id from "Input Id to classify"

### Sentiment analysis
- Input field "Enter text you want to analyse" chooses what text to analyse
- Button "submit" returns score and saves the result in database
- Button "Click here to view data" shows previous results from the database
- Input field "Enter ID" is to rerun previously inputed data without submiting it again
- Button "submit" displays the result
- 


# Installed packages
- Python=3.9
- streamlit==0.88.0
- numpy==1.21.2
- starlette==0.14.2
- requests==2.26.0
- transformers==4.10.0
- uvicorn==0.15.0
- pydantic==1.8.2
- pandas==1.3.3
- fastapi==0.68.1
- Pillow==8.3.2
- torch==1.9.0
- torchaudio==0.9.0
- torchvision==0.10.0
- python-multipart==0.0.5


