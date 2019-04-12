# DEVOPS PYTHON/JS CODING CHALLENGE

This project is a solution to a problem posed by a potential employer.  I noted their use of Flask so ventured into a bit of the unknown (normally end up in Django land tbh!) and this is the result.  It's a microservice API to some freely available traffic data, specifically this: http://api.dft.gov.uk/v3/trafficcounts/export/la/Devon.csv.

## DEMOS

### Simple JS Client:

http://flatcoder.co.uk:5101/

### API Endpoints:

http://flatcoder.co.uk:5101/regions
http://flatcoder.co.uk:5101/authorities
http://flatcoder.co.uk:5101/roads
http://flatcoder.co.uk:5101/junctions
http://flatcoder.co.uk:5101/categories
http://flatcoder.co.uk:5101/links
http://flatcoder.co.uk:5101/counts

All endpoints ALL support an optional "perpage" and "page" paramater.  E.g.:

http://flatcoder.co.uk:5101/counts?perpage=5
http://flatcoder.co.uk:5101/counts?perpage=5&page=1

Traffic counts support "order" and "order_by" for length and total count:

http://flatcoder.co.uk:5101/counts?order_by=length&order=asc
http://flatcoder.co.uk:5101/counts?order_by=total&order=desc

Traffic counts support filtering on a specific CP

http://flatcoder.co.uk:5101/counts?cp=10

Combination examples:

http://flatcoder.co.uk:5101/counts?order_by=total&order=desc&perpage=5&page=0
http://flatcoder.co.uk:5101/counts?order_by=total&order=desc&perpage=5&page=0&cp=10

## TECH STACK

Python 3.7, Flask, Flask Script, Flask Migrate, Flask API, Jsonify, SQL Alchemy (currently using Postgres).

## DEPLOYMENT OPTIONS

Docker compose (recommended), pure Docker, Python virtual environment, Full local install (not recommended).

## INSTALLATION

The simplest and quickest way is to use docker compose to fire up 2 containers (DB and Web server).  From the project directory, simply run:

    docker-compose up --build

The (Flask dev) web server will be available locally via port 5101.  The (Postgres) database server can be reached via port 5532.  I chose to remap the default ports since you may, like I, already have a running instances of Postgres or Flask locally.

Included is an "env.sample" file............ copied to .env vi Docker......................., for database credentials.  Normally this wouldn't be checked into version at all, but for the purposes here it simply sets the defaults on the container...................easy deploy.....................still demonstrates the separation of credentials.  For data persistence, note the commented "volumes" lines in docker.compose.yml that will keep data even if the container is destroyed.

If, for some reason, docker compose is not an option, it ought to be possible to fire up separate containers manually.  E.g.:

    docker run --rm --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5532:5432 -v ./pg_data:/var/lib/postgresql/data postgres

If Docker is not available at all, the project can still be run using a Python 3.7 virtual environment + pip install -r requirements.txt + database migration/import using the management interface described below.

## MANAGEMENT INTERFACE & IMPORTER

Provided by "manage.py".  Generally, no need to run any of the below if you're using Docker (as it's automated).  If you must, you'll likely need to use "docker exec" to jack into the Matrix.

    database            Perform database migrations
    import_csv          Imports the Road Traffic Count (CP) data
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

You can follow any command with "-?" to see help / options.

## SOLUTION DISCUSSION

Observations surrounding the provided data as follows:

- A road has a name. A road can be in multiple categories (e.g., it may span urban and rural).
- Road categories have a unique code and a description.
- Traffic counts are made at an easting/northing on a road with a start/end junction.
	- Junction start/end pairs are identified by a CP.
- CPs are within a local authority which is within a region.
- CPs are only unique within any given year.
- Two junctions linked together, I am presuming, the length can vary over time as roads change.

Models were built and further considerations emerged in the process:

- Conversions. Conclusion is it's best client side for now (if needed at all).  There's a data integrity issue if we store both KM and Miles per row (someone edits a row, changes Miles but not KM....).  But, there's a big performance overhead if we start applying conversions row by row server side.

- Totals are a different problem.  Typically, I'd say "don't store what you can calculate" for all the same reasons as conversions above, as it breaks database normalisation rules.  However... totals may be critically important to the API ("get me all roads with a total vehicle count greater than......").  The resulting performance hit would be server side this time, as Postgres applied "SUM" row by row.

- Currently, we *ARE* storing totals, but I'd revisit this especially if the data is not to stay READ ONLY or if much larger data sets are planned (this set is quite small really).  An aggregated column could be used (SQL Alchemy Utils), solving integrity issues, but not performance.  Triggers are an option, to address performance (read, not write), but are usually not database agnostic.  Again, worth a revisit this one.

The resulting database model in included in this repo (see schema.png):

![alt text](https://github.com/flatcoder/cityscience/raw/master/schema.png "Data Model")

NOTE: This is all currently using the Flask dev web server.  In production, look to Apache or Nginx.  Choose your poison, but know this... Microsoft IIS is deadly and it will probably kill you.

## ENHANCEMENTS

A little more time could greatly extend the API, the hardwork is done.  Would be worth including some automated testing (Python unittest) and CI (perhaps Travis CI).  For now, however, I think there's enough to show the direction headed!  Oh, and it still irks me storing totals!  Peace. :)
