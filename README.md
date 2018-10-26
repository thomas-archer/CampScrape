# CampScrape
Checks for availalbe campsites and notifies user with reservation links.

Campsites at popular campgrounds can be almost impossible to reserve, especially on short notice. Recreation.gov allows campers to book either online typically up to six months in advance. It can be difficult to plan trips that far in advance, but popular locations such as Yosemite will become fully booked in days. Without a waitlist or notification system built into their system, the only way to secure a campsite from a fully booked campground on short notice is to periodically refresh and check the page for any possible cancellations.

CampsScrape automates this process for the user and allows them reserve campsites ASAP. Given a date range and specified campground, it'll web scrape the reservation.gov website for available sites and notify the user via slack, email, or desktop

It can be run via cronjob to check for available sites as often as the user desires. I typically run it remotely using an AWS EC2 instance to consistently run it every five minutes. Overall it works great for finding campsites at popular campgrounds the week-of as people often cancel their reservation within the week leading up to their trip.
