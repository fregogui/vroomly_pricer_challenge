# Vroomly pricer challenge


## Guidelines

- initialize a git repo in this folder
- once you are done, export the git repo using `git bundle create vroomly_pricer_challenge_<Your Name>.gitbundle --all` and share the bundle with us


We are interested in code that is:

- clean
- extensible
- robust


The preferred language is Python 3 as it is the language we have most expertise in
but another may be used if you are not familiar enough with Python.


## Statement

The goal is to develop an algorithm to compute the parts price for a given vehicle
and a given intervention (ex: brake pad replacement on a Peugeot 307 1.4 16V).

## Input

Input data is provided to you in the form of multiple CSV files located in the `data` directory.

- `vehicles.csv`: a collection of occurrent vehicles (on the French market)
- `articles.csv`: a collection of automotive parts
- `article_vehicle_relations.csv`: a mapping of which article is compatible with which vehicle
- The `catalogs` directory contains price catalogs for the articles from different sources

The interventions which must be supported by the pricer are:

- "Front brake pads replacement", slug: `front_brake_pads`
- "Front brake rotors and pads replacement", slug: `front_brake_rotors_and_pads` (when changing discs, pads are always replaced)
- "Oil change", slug: `oil_change`
- "Fuel injectors replacement", slug: `injectors`

Their specifics are detailed in the next section.


## Business rules

### Front brake pads replacement

Brake pads are part of the disc braking system, they are a consumable as they wear when braking.
Worn down brake pads will greatly decrease braking performance and will
end up damaging the brake rotors and pistons.

When replacing brake pads, both sides of the car are done at the same time as they wear
at a similar rate, this means that a replacement requires four new articles as there are two pads
per side.


### Front brake rotors and pads replacement

Another component of the disc braking system is the rotor (or disc), it too wears and then
needs replacement though at much greater intervals.

Pads are always replaced when replacing rotors
as it does not require more labour and the parts are cheap. For the same reason as for pads, both
sides of the car are replaced at the same time which requires two new rotors and four new pads.

### Oil change

Oil is required to lubricate the moving parts inside a combustion engine. As engines are not perfect,
the oil gets dirty during operation (because combustion chambers are never perfectly sealed for example),
dirty oil will damage an engine in the long run (acting as a abrasive) so regular changes are
required.

Different engines use different types of oil, in the context of this exercise, this is determined by the following table:


| Oil type | Production year  | Price (€/liter) |
|----------|------------------|----------------:|
| 10W40    | < 2002           | 5.00            |
| 5W40     | 2002 <= y < 2007 | 6.00            |
| 5W30     | \>= 2007         | 8.00            |


The cost of parts for an oil change is function of the volume of oil in the engine and the volumic price
of the type of oil used.

To ensure the oil stays cleaner longer, engines also include an oil filter. Oil filters always
get replaced when the oil gets changed.


### Fuel injectors replacement

Fuel injectors are a critical part of the combustion engine, they are responsible of spraying the
fuel in the combustion chamber in a way that ensures an even combustion (the more even the
 distribution, the better the fuel is mixed with air, the more can be get burned during each cycle).

There is one injector per cylinder so when replacing them the number of parts required depends on
the engine.

Diesel engines do not use the same injectors as petrol engines as they require a much greater fuel
pressure to allow sparkless ignition of the fuel.

Note that in reality, injectors are most often replaced one by one and not all at the same time as they
are not a consumable and replacement is due to a defect, not wear. In the context of this exercise, we replace all of them.

### Price selection

There may be multiple priced articles matching an article type on a vehicle, in the context of this exercise
 we choose to use the median price.

## Expected output

A Python file callable from the command line that supports the following parameters :
- `--intervention` the slug of the chosen intervention (`front_brake_pads`, `front_brake_rotors_and_pads`, `oil_change` or `injectors`)
- `--vehicle` the id of the chosen vehicle

and outputs the parts price. 

ex : `> python pricer.py --intervention front_brake_pads --vehicle 1234`
