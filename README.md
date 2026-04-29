Backend:
  http://localhost:8000

Frontend:
  http://localhost:5173


  
----Patterbuster

pip freeze > requirements.txt

source patterbuster/bin/activate

uvicorn main:app --reload


----Apollo server (Main)
node index.js

----client
npm run build && npm run start