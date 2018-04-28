Python-to-TeX photo calendar (ptpcal.py)
========================================

Usage
-----

1. (optional) Download holiday list from
   https://www.schulferien.org/deutschland/ical/.  
   The list should be an iCalendar (RFC 5545) file with event elements for each
   day that should be marked as a holiday (bold blue font in the default
   template). Multi-day events are supported and will mark all days they fully
   span.

2. Select 12 photos and store them as `month01.jpg` to `month12.jpg` in the
   working directory. (PNG or PDF files can be used as well.)

3. Set year, language, and the path to the holiday file in `ptpcal.py`:

        year = 2018
        locale_str = 'de_DE.utf8'
        holiday_ics_file = 'holidays.ics' # will be ignored if the file does not exists

4. Run `ptpcal.py` and store output in a (temporary) file:

        ./ptpcal.py > calendar_2018.tex

5. Compile output file using LuaLaTeX:

        lualatex calendar_2018.tex

TODOs
-----

- [ ] Get parameters (year, language, paths to holiday file and photos) from
  commandline parameters instead of hardcoding them.

The script is sufficiently usable in its current form, so these might take "a
while" to be implemented.

License
-------

The source code of `ptpcal.py` is made available under the [Apache License
2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

The example photo is made available under the [Creative Commons Attribution
Share Alike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
License.
