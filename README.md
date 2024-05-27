this is a simple Task-Managing page in which you can add tasks, remove them and mark them as done 
it is a proof of concept page that works with localstorage only

the app utilizes Local storage to save task state, JW tokens and User info as well as the theme of the app.

For Api Documentation and visualization i Used Swagger library as seen here:
![image](https://github.com/Drkiller325/API-Localstorage/assets/90339098/d707c70f-6c4b-41f6-b105-1883e8419094)
As you can see i have an Authoriziation login and register request that i use to save the users credentials and for password and site safty i generate a JW token for verification
as well as the 4 CRUD Functions which are 
1. Create: in this case we have a post request that adds a Task in the app:

![image](https://github.com/Drkiller325/API-Localstorage/assets/90339098/82740388-d01d-40d4-ae50-5aef0b54dc21)

as you can see in the frontend side we have an admin and a client which have different permessions accordingly

3. Read: any user can see the currently created tasks by sending a simple get request
![image](https://github.com/Drkiller325/API-Localstorage/assets/90339098/b4b5636f-bac9-44ba-9a3e-28c46c5ae5df)


4. Update: the update method is a post method that allows the user to modify the state of a task from undone-Done as seen below
![image](https://github.com/Drkiller325/API-Localstorage/assets/90339098/96d30628-3908-42de-b229-35450600d96f)

5. Delete: the Admin is the only user that has permession for deleting, creating or adding tasks to the list ad when the X is pressed the task is gone




