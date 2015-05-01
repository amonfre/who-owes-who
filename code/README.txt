Instructions for running our code:

If you don't have virtualenv installed on your VM, 
please run the following command to install:
pip install virtualenv 

Then, from you terminal window:

1. Go to our project folder (cd who-owes-who/code/interface)
2. use the following commands:
virtualenv env
3. source env/bin/activate
4. pip install Django==1.8
5. python manage.py migrate
5. python manage.py runserver
6. Go to the specified server on a web browser
7. Explore the website:


- Our video has a demo of the website that includes a run-through of most of the
functionalities of the website.

- If you go to the Control on the left-side panel, you can use the buttons
"Simplest example" and "Random example" to generate friends. If you go to
Graph view, you can see the visualized graphs with random transactions just created. 

c) The New Transaction panel lets you create a new transaction and specify if
you want to loan or borrow, the amount and the friend that you are making this
transaction with. To submit the transaction, you need to know your friend's username 
for verification purposes. 

d) Transaction History displays your previous completed and pending transactions. 
It also allows you to cancel a transaction request or accept a friend's transaction request.

e) The Profile allows you to write a short blurb about yourself that will be visible to others.

f) The Graph View visualizes all the transactions.

g) In the control panel, you can choose the algorithm you want to use to optimize your trnasaction:
friendly or greedy. Then the computed graph view will visualize the optimized transaction view. 


