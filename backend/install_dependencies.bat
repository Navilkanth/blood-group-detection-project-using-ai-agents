@echo off
echo ========================================
echo Installing Blood Group Classification
echo Backend Dependencies
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
echo This may take several minutes...
echo.

pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install python-dotenv==1.0.0
pip install Pillow==10.0.0
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install scipy==1.11.2
pip install tensorflow==2.13.0
pip install torch==2.0.1
pip install torchvision==0.15.2
pip install scikit-learn==1.3.0
pip install SQLAlchemy==2.0.20
pip install cryptography==41.0.3
pip install werkzeug==2.3.7
pip install requests==2.31.0
pip install python-dateutil==2.8.2

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run the backend with:
echo   python app.py
echo.
pause
