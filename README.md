<style>
blue { color: #0277bd }
</style>

# Shediac Bay Yacht Racing Association (SBYRA) documentation

*SBYRA is a single user group application as part of a larger application in development (WINCH) for yacht and regatta management*

## 1. Basic Implementation: 

- App allows users to register their yachts for the local racing club and events. Admin staff can create regatta events and event series to track all racing data and results. 
- Weather app connects to an API to display and register weather data at various current and event times.
- Main web interface allows users and non-users to view event results and browse public yatch and event info.

## 2. Future additions:

- Local chat feature
- Local buy & sell feature
- result visualisation 

## 3. Contributors:

Julien Boudreau - Creator, Lead Developer, Lead UI and UX Design. 

## Project Structure:

sbyra_src
  - accounts (User, Profile)
  - racing (Yacht, Series, Event, Result )
  - weather (openweathermap.org api call)
  - tests (pytest testing suite)
  - settings.py
  - urls.py


manage.py

## Racing Model Schema:

Staff <blue>Users</blue> create <blue>Series</blue> to hold a set of regattas or racing events (yearly, monthly, weekly, etc.). Once a series is created, various events can be added, modified and evaluated. The <blue>Event</blue> has a ForeignKey relationship to the <blue>Series</blue>. <blue>Yacht</blue> and <blue>Event</blue> have a Many to Many relationship linked by a through table <blue>Result</blue>. The <blue>Result</blue> table contains individual yacht results for various events. 

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