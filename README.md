# Project Structure
This work showcases a simple implementation in Python showcasing interaction with the AirspaceLink API's that I think are wonderful and of relevance to this demo.
One creates a multistop route, as drones don't typically fly from one location to another. AirspaceLink interaction is in terms of routing to those desired points 
of a route around no fly zones, i.e. schools, prisons, shopping malls. (shopping malls and prisons are indivisible to me).

This code works with the InterUSS open example listed below. 
This code employs the use of the ESRI Javascript API in 3D. The application starts in South Lake Tahoe, California, which was home. No other reason. 

This work requires an instance of the DSS to be running. 
To run the DSS locally:

1: Start Docker
2: Clone an instance of the DSS (clone from here: https://github.com/interuss/dss)
3: Within the local repo, navigate to dss/build/dev. 
4: Run this command in terminal:
    % sudo ./run_locally.sh up

    NB: to stop it run:
    control + c

    To remove it completely from docker run:
    % sudo ./run_locally.sh down


This project contains 7 subdirectories. 

Open the Tests directory.

Open app.py and run it as Python: Flask

This will create a web application:
http://127.0.0.1:5000
If you navigate to this url you will see:
“Welcome to the AirspaceLink InterUSS Web Application”

Navigate to:
http://127.0.0.1:5000/route_map to get the interactive map. To edit this webpage in VSCODE, you'll find the file /Tests/templates/index.html, with all the javascript that runs that page.

To expose this to outside of localhost, you need ngrok.

Install ngrok via Homebrew with the following command:
brew install ngrok/ngrok/ngrok

Run the following command to add your authtoken to the default ngrok.yml configuration file. You should log into NGROK for the next part so you can get the correct authtoken:

ngrok config add-authtoken <token>

Deploy your app online:

Ephemeral Domain
Put your app online at ephemeral domain Forwarding to your upstream service. For example, if it is listening on port http://localhost:8080, run:
ngrok http http://localhost:8080

so in our case we run:
ngrok http http://127.0.0.1:5000

When you run it you will be given a display
ngrok                                                                                                                    (Ctrl+C to quit)
                                                                                                                                         
Take our ngrok in production survey! https://forms.gle/aXiBFWzEA36DudFn6                                                                 
                                                                                                                                         
Session Status                online                                                                                                     
Account                       Edan Cain (Plan: Free)                                                                                     
Version                       3.6.0                                                                                                      
Region                        Australia (au)                                                                                             
Latency                       64ms                                                                                                       
Web Interface                 http://127.0.0.1:4040                                                                                      
Forwarding                    https://8797-2406-2d40-72ab-5910-902-dee6-d0a0-af4c.ngrok-free.app -> http://127.0.0.1:5000                
                                                                                                                                         
Connections                   ttl     opn     rt1     rt5     p50     p90                                                                
                              0       0       0.00    0.00    0.00    0.00   

Take the value for forwarding: 
https://8797-2406-2d40-72ab-5910-902-dee6-d0a0-af4c.ngrok-free.app/route_map
Paste it into a browser, you will be prompted for confirmation, say yes. Now you are looking at the route_map exposed to the web.
