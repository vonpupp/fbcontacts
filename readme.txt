    Creates a CSV file with facebook contacts data (name and email) from yahoo TrueSwitch

    PROCEDURE:
        * Requirement: You need a yahoo & hotmail mail account, create them if needed.
        
        AT HOTMAIL:
        * At hotmail go to people (up left corner)
        * Click on the Facebook icon
        * Click on okay, to authorize facebook to share contacts data with hotmail
        
        AT YAHOO:
        * At yahoo mail go to contacts
        * Click on Import contacts
        * Click on the hotmail icon
        * Put your credentials and check "I give Yahoo! permission..."
        * The "Step 2" window will show you a list of your contacts. Save the page with save page as
        * It will create a /transfercontacts_files folder with an index.html file within
            This is going to be the program input!

    Command Line Usage:
        python fbcontacts.py ./transfercontacts_files/index.html
        
    Author:			Albert De La Fuente (www.albertdelafuente.com)
    E-Mail:			http://www.google.com/recaptcha/mailhide/d?k=01eb_9W_IYJ4Pm_Y9ALRIPug==&c=L15IEH_kstH8WRWfqnRyeW4IDQuZPzNDRB0KCzMTbHQ=
    
    Why I've done this:         I've done this because I believe that I own my fb account data,
                                and I should be able to export it if I want.
