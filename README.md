# Shediac Bay Yacht Racing Association (SBYRA)

*SBYRA is a single user group application as part of a larger application in development (WINCH) for yacht and regatta management*

## 1.Basic Implementation: 

- App allows users to register their yachts for the local racing club and events. Admin staff can create regatta events and event series to track all racing data and results. 
- Weather app connects to an API to display and register weather data at various current and event times.
- Main web interface allows users and non-users to view event results and browse public yatch and event info.

## 2.Future additions:

- Django Sessions
- Local chat feature (async chat)
- Local buy & sell feature (forum)
- result visualisation (charts)

## 3.Tech stack

- Python Django
- Pytest-Django
- HTML / HTMX
- Tailwind CSS
- JS AlpineJS
- PostresQL

## 4.Contributors:

Julien Boudreau - Creator, Lead Developer, Lead UI and UX Design. 

## 5.Project Structure:

sbyra_src
  - accounts (App - User profiles and authentication)
  - api (Django Rest Framework API)
  - content (App - blog, articles, static web content)
  - demo (run demo from cmd line)
  - racing (App - all racing related functionality)
  - weather (App - openweathermap.org api call)
  - tests (pytest testing suite)
  - settings.py
  - urls.py

#### templates (all HTML templates)
#### manage.py 


## How it all Works - The Racing Model Schema:

Regular User: A user can create a yacht and register for various Regatta series and events. 

Admin User: An Admin User can create Series to hold a set of regattas or racing events (yearly, monthly, weekly, etc.). Once a Series is created, various events can be added, modified and evaluated. The Event has a ForeignKey relationship to the Series. Yacht and Event have a Many to Many relationship linked by a through table Result. The Result table contains individual yacht results for various events. 

The core of the project relies on the Racing app schema and the Result table. The Result table links an individual Yacht to an individual Event. As an Event has varying start times for different yacht racing classes, the Result table provides the logic to determine the final result based on a yacht's start time (assciated to it's class), finish time and phrf rating. A time correction algorithm in the Result calcultes the results following;

    Corrected Time Algorithm:

    1. Establish start time based on yacht_class
    2. Convert start time and finish time to seconds for further processing
    3. Calculate elapsed time in seconds between start time and finish time
    4. Apply time correction factor based on phrf_rating and known formula
    5. Convert corrected time above (seconds) into datetime.time object for model TimeField()
    6. Save final datetime.time object into Result.posted_time

### Basic Queries:


The Yacht class has two managers, allowing filtering for active status. Both contain additional methods to filter by yacht class:

```
Yacht.objects.all()
Yacht.active.all()
```

* All active yachts (two managers with additional methods):
```
Yacht.objects.active()
Yacht.active.all() 
```
* Filter all yachts by class:
```
Yacht.objects.by_class('X') 
```

* Filter active yachts by class:
```
Yacht.active.by_class('X')
```

## Run Demo: 

1. Clone repository in project folder
2. Create your virtual environment
3. Install requirements.txt 
4. Create a superuser
5. Run demo in shell: 

```
py manage.py unleash_demo
```
* Note that an API key for openweather.org is required for weather context processor to function