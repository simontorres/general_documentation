#
#                       A d a s s  C h e c k s . p y
#
#  This is the code for a module that contains a number of checking
#  routines that are potentially used by a number of scripts involved in
#  editing the ADASS proceedings. Over time the interfaces to these routines
#  have evolved to make the routines more flexible, generally through the
#  addition of optional parameters. A number of these routines take one or more
#  of a fairly standard set of optional parameters.
#
#  Common optional parameters:
#     TexFileName can be used to supply the name of the .tex file, instead
#                 of assuming it will be the paper name with a .tex extension.
#     BatchMode   can be set true to indicate the routine is being called from
#                 a batch program and should not print out diagnostics as it
#                 might if it were run more interactively. Usually, if BatchMode
#                 is true, diagnostics can be appended to a list such as
#                 Problems, also passed as an optional argument.
#     Problems    can be used to pass a list of strings, to which the routine
#                 can add descriptions of any problems it encounters.
#     Warnings    can be used to pass a list of strings, to which the routine
#                 can add warnings about any questionable issues it encounters.
#
#
#  VerifyRefs (Paper,AllowBibitems = True,TexFileName = "",BibFileName = "",
#                                       Problems = None, Warnings = None)
#     Checks that the references used in the main .tex file and those
#     in the .bib file are consistent. It accepts references defined in the
#     .tex file using \bibitem for purposes of consistency checking, but
#     warns about these. This can be controlled using the optional parameter
#     AllowBibItems. BibFileName can optionally be used to explicitly specify
#     the name of the .bib file.
#
#  VerifyEps (Paper,TexFileName = "",Problems = None,Warnings = None)
#     Checks that any graphics files used in the main .tex file are
#     supplied, and that any graphics files supplied are used by the
#     main .tex file.
#
#  CheckPackages (Paper,TexFileName = "",Problems = None)
#     Checks any packages used by the main .tex file, and notes the use of
#     any standard packages - these can be included, but it's unnecessary -
#     and warns about any non-standard packages.
#
#  GetBibFileRefs (BibFileName,BatchMode = False)
#     Returns a list of strings giving the names of the various references
#     defined in the named .bib file.
#
#  TrimBibFile (Paper,Keep = True)
#     Looks in the .bib file used by the main .tex file and comments out
#     any unused references. It assumes the .bib file has the same name as
#     the common .bib file returned by GetBibFileName(). If the optional
#     Keep argument is False, the unused references are deleted rather than
#     just commented out.
#
#  GetAuthors (Paper,Notes,TexFileName = "")
#     Looks in the main .tex file and generates a list of the authors
#     suitable for generating \aindex entries.
#
#  FixCharacters (Line,LineNumber)
#     Replaces any of the common non-printable accented characters in a line
#     with the LaTeX equivalent sequence and returns the corrected line.
#
#  CheckCharacters (Line,LineNumber,Problems = None)
#     Is a version of FixCharacters that only checks for non-printable
#     characters rather than actually fixing them..
#
#  CheckRunningHeads (Paper,TexFileName = "",Problems = None)
#     Checks for a number of common errors in the way the running heads
#     for the paper are specified using \markboth.
#
#  GetArchiveList (Path,Paper)
#     Looks in the specified path for any archive file that might be being
#     used for the specified paper and returns a list of such files.
#
#  GetArchiveTime (Filename,FileList = None)
#     Returns the latest modification date (as a time in seconds since the
#     epoch) of any file contained in the named archive file. If passed an
#     optional list, it will add the names of all the files it finds to that
#     list.
#
#  GetBibFileName() returns a string giving the name of the common .bib
#     file used for all the papers, eg "adassXXVreferences.bib".
#
#  AuthorChars (Author) returns a simplified version of an author's surname,
#     with any accenting LaTeX directives removed.
#
#  GetConferenceNumber() returns a string with the Romal numerals for the
#     current ADASS conference, eg "XXV".
#
#  GetEditors() returns a string giving the names of the editors of the
#     current Proceedings, in a form suitable for a .bib file entry.
#
#  GetVolume() returns the number of the current ADASS volume - the ASP
#     volume number, as needed by a .bib file entry.
#
#  CheckCite (Paper,TexFileName = "",Problems = None)
#     Checks to see if the specified paper is using any \cite commands
#     instead of the preferred comamnds \citep, \citet etc.
#
#  History:
#     16th Feb 2016. Now checks for all natbib \cite options. KS.
#     19th Feb 2016. Added GetAuthors() (and AuthorScanCallback()). KS.
#     22nd Feb 2016. Fixed recently introduced problem generating message
#                    about a "\cite" reference. TrimBibFile() is now a
#                    little cleverer about locating the end of an entry. KS.
#     29th Feb 2016. Added FixCharacters(). KS.
#      1st Mar 2016. Had managed to lose the test for lower case initial
#                    letters (generally an indication something has gone
#                    wrong) in GetInitial(). Fixed. KS.
#      3rd Mar 2016. AuthorScanCallback() now allows for forced line-breaks -
#                    "\\" or "\\*". KS.
#      4th Mar 2016. Added GetArchiveTime(). Also fixed a problem where
#                    TrimBibFile() was not stripping blanks from the ends of
#                    references before comparing them. Really, RefScanCallback()
#                    should return references ready stripped, which would 
#                    allow both RefCheck() and TrimBibFile() to get rid of
#                    a number of calls to strip(). KS.
#      7th Mar 2016. Added GetArchiveList(). KS.
#      8th Mar 2016. GetArchiveTime() no longer fails if an archive contains
#                    links to files that don't exist. KS.
#     29th Mar 2016. Fixed diacritical tilde problem in author names. KS.
#      1st Apr 2016. Added GetBibFileName() and CheckPackages(). KS.
#      4th Apr 2016. Added AuthorChars(), GetConferenceNumber(), Editors() and
#                    Volume(). KS.
#      6th Apr 2016. Corrected a couple of .index() calls that should have
#                    been .find(), so they don't raise exceptions if the string
#                    isn't found. KS.
#      7th Apr 2016. Improved parsing in GetBibFileRefs() so it can handle
#                    cases where the reference type and name are not all
#                    specified on the first line of the reference. 
#                    TrimBibFile() still has problems with such files, but at
#                    least it now prints out a warning when this happens. KS.
#     28th Apr 2016. Fixed problem in author list parsing caused by extraneous
#                    trailing blanks, which was generating an erroneous 
#                    possible missing comma warning. KS.
#      7th May 2016. Added check for upper case characters in body of surname
#                    when collecting author names. KS. 
#      8th May 2016. The author name scan code now tries to spot both the
#                    'Spanish surname' case and the 'on behalf of the team'
#                    case, and makes a note of a possible problem. KS.
#     23rd May 2016. RefCheck no longer complains that a .eps file is not
#                    used if the .tex file does use it but has allowed the 
#                    extension to default to .eps. KS.
#     24th May 2016. Now allows 'le' as part of a surname. KS.
#      7th Jun 2016. Now checks for surnames that don't seem to have any
#                    associated initials. KS.
#     14th Sep 2016. VerifyEps() now returns an overall status value and takes
#                    an optional main .tex file name. The same change has been
#                    made for CheckPackages(). KS.
#     18th Sep 2016. VerifyRefs() now takes a number of additional optional
#                    arguments, and returns an overall status value. The
#                    GetAuthors() routine now also takes an optional main
#                    TeX file name. KS.
#     20th Sep 2016. Added CheckCharacters() and CheckRunningHeads() and
#                    CheckCite(). KS.
#     23rd Sep 2016. Check on author names now no longer complains about
#                    the capital in Scottish names like MacDonald. KS.
#     23rd Nov 2016. Modified the conference details so they apply to the
#                    2016 Trieste conference. KS.
#     27th Nov 2016. GetArchiveTime() now allows for spaces and quotes in the
#                    names of archive files or their directories. Also now 
#                    ignores __MACOSX files when counting files to see if there
#                    is just a single sub-directory at top level. KS.
#      9th Dec 2016. Added support for 'batch mode' operation - eg when
#                    used by PaperCheckBatch.py - to VerifyRefs() and to
#                    VerifyEps(), CheckCharacters(), CheckPackages(),
#                    CheckCite(), GetTexFileRefs() and CheckRunningHeads(). KS.
#     10th Dec 2016. CheckPackages() now allows "./asp2014". KS.
#     19th Dec 2016. GetArchiveTime() can now optionally return a list of the
#                    files in the archive and ignores the dates on any files
#                    that are directories. (It really ought to do a proper
#                    recursive search through the file structure.) KS.
#     18th Feb 2017. Changed the mapping of the unprintable character 0xd5.
#                    See comments to FixCharacters{} for more detail. KS.
#     25th Mar 2017. VerifyRefs() and TrimBibFile() now use the new routine
#                    FindBibFile() to fall back on <paper>.bib as the name
#                    for the .bib file if the standard .bib file cannot be
#                    found. KS.
#     14th Jul 2017. VerifyEps() now checks for file names that match but only
#                    if case is ignored. KS.
#     16th Jul 2017. RunningHeadsCallback() now checks the running title against
#                    that from the current template and the older template. KS.
#     17th Jul 2017. VerifyEps() now checks subdirectories as well as the
#                    default directory for graphics files. If graphics files
#                    are in subdirectories, it regards this as a problem. The
#                    highlighting used for problem logging in this routine is
#                    now a little more consistent. KS.
#     24th Jul 2017. GetBibFileRefs() now checks for - and ignores - unexpected
#                    entry types. Updated the routine descriptions at the start
#                    of this file to include the various optional parameters
#                    that have been added over time. VerifyEps() now checks for
#                    files specified in the .tex file with leading "./", and
#                    now checks for image files used more than once in the
#                    .tex file. Improved the way VerifyRefs() handles the case
#                    where a .bib file is supplied, but the .tex file has a
#                    \bibliography entry that specifies the wrong name. KS.
#     25th Jul 2017. Improved VerifyRefs() diagnostics where a .tex file has
#                    no citations at all. Discovered BibTeX doesn't ignore
#                    unexpected entry types, so now GetBibFileRefs() only warns
#                    about them. The original problem ignoring them was supposed
#                    to solve is now solved by resetting the parser on lines
#                    that start with '@'. KS.
#     26th Jul 2017. Corrected spacing in "will default to .eps" message. Now
#                    tries to pick the case where an author name has been given
#                    with the surname first instead of last. FindBibFile() now
#                    looks for any .bib file in the directory if it cannot find
#                    the one it expects, and reports on what it found. The
#                    code that checks author names now allows 'da' as part of
#                    a surname - eg "da Silva". KS.

import sys
import string
import os
import tempfile

import TexScanner

# ------------------------------------------------------------------------------

#                 A d a s s  C o n f e r e n c e  D e t a i l s
#
#  These should be the only items in the ADASS proceedings Python modules that
#  needs to be changed from year to year. (Note that these are not used by the
#  PaperCheck.py script distributed with the manuscript instructions. They are
#  used by the various utility scripts used in the editing process for the
#  proceedings.)

__AdassConference__ = "XXVI"

__AdassEditors__ = \
             "Pasian,~F. and Molinaro,~M. and Mansutti,~O. and Shortridge,~K."

__AdassVolume__ = "TBD"

# ------------------------------------------------------------------------------

#                   G e t  C o n f e r e n c e  N u m b e r
#
#   Returns the ADASS conference number in Roman numerals.

def GetConferenceNumber() :

   return __AdassConference__
   
# ------------------------------------------------------------------------------

#                         E d i t o r s
#
#   Returns a string giving the typeset names of the editors of the ADASS
#   proceedings in a form suitable for a BibTeX entry.

def Editors() :

   return __AdassEditors__
   
# ------------------------------------------------------------------------------

#                         V o l u m e
#
#   Returns a string giving the volume number for the ADASS proceedings in 
#   a form suitable for a BibTeX entry.

def Volume() :

   return __AdassVolume__
   
# ------------------------------------------------------------------------------

#                      G e t  B i b  F i l e  N a m e
#
#  GetBibFileName() returns the name of the common ADASS .bib file being used.
#  Conventionally, this varies depending on the conference number, being
#  "adass<conf>references.bib", where <conf> is the conference number in
#  Roman numerals.

def GetBibFileName() :

   return ("adass" + __AdassConference__ + "references.bib")

# ------------------------------------------------------------------------------

#                         E x t r a c t  R e f s
#
#  ExtractRefs() is a utility routine for VerifyRefs() which looks at a list
#  of the words found in a LaTeX \cite -type directive and returns the
#  list of what seem to be the actual references - it assumes these are
#  in the first non-optional argument (in {braces}) and are separated by
#  commas.

def ExtractRefs (Words) :
   Refs = ""
   for Word in Words[1:] :
      if (Word != "") :
         if (Word[0] == '{') :
            Refs = Word.strip("{}")
            Refs.replace(" ","")
            RefList = Refs.split(",")
            break
   return Refs

# ------------------------------------------------------------------------------

#                        G e t  B i b  F i l e  R e f s
#
#   Looks in the current directory for the  specified .bib file, and
#   returns a list of all the references it defines.

def GetBibFileRefs (BibFileName,BatchMode = False):

   #  Later versions of Python have better support for enums, but this
   #  works on old versions too.
   
   def enum(**enums):
      return type('Enum', (), enums)
   
   #  These parse states are fairly simplisitic, and really assume that
   #  the bib file is valid and laid out in a relativly straightforward way.
   #  Most files will just have a line at the start of each reference
   #  @type{name,
   #  and in this case we go through all the states in the one line.
   #  If the file starts with
   #  @type{
   #     name,
   #  then the first line will take us from needing an @ to needing a 
   #  comma, and the second line will provide the reference and move us
   #  back to needing an @. 
   #  If the file starts with
   #  @type
   #     {name,
   #  or even
   #  @type
   #  {
   #      name,
   #  Then successive lines take us to needing a brace, then needing a 
   #  comma, then getting the reference and back to needing an @.
   #  Anything else it won't handle properly. And it won't pick up cases
   #  where there's someting before the '@' on a line, and will get confused
   #  if the reference is incomlete, without a closing brace, say.
   
   States = enum(NEED_AT = 0, NEED_BRACE = 1, NEED_COMMA = 2)
   
   #  The set of expected entry types
   
   ExpectedTypes = ["article","book","booklet","conference","inbook",
                  "incollection","inproceedings","manual","mastersthesis",
                  "misc","phdthesis","proceedings","techreport","unpublished"]
   
   BibFileRefs = []
   State = States.NEED_AT
   Found = False
   if (os.path.exists(BibFileName)) :
      BibFile = open(BibFileName,mode='r')
      
      for BibFileLine in BibFile :
      
         #  There are some odd .bib fies around that this code doesn't parse
         #  properly, and we can end up still looking for something in a
         #  reference definition when we hit a line that starts with '@'.
         #  It's more likely that we've mis-parsed the file than that
         #  there is such a line in the middle of a legitimate reference,
         #  so we restart at this point.
         
         if (BibFileLine.strip().startswith('@')) : State = States.NEED_AT
      
         #  In most cases, we'll be looking for the '@' that starts a
         #  reference definition, and will find all we need on the one line.
         #  If not, we end up in one of the intermediate states.
         
         if (State == States.NEED_AT) :
            BibFileLine = BibFileLine.strip().rstrip("\r\n")
            if (BibFileLine.startswith("@")) :
               State = States.NEED_BRACE
               Brace = BibFileLine.find("{")
               if (Brace > 0) :
                  EntryType = BibFileLine[1:Brace]
                  State = States.NEED_COMMA
                  Comma = BibFileLine.find(",")
                  if (Comma > 0) :
                     Ref = BibFileLine[Brace + 1:Comma].strip()
                     State = States.NEED_AT
                     BibFileRefs.append(Ref)
               else :
                  EntryType = BibFileLine[1:]
      
               #  Check the entry type and warn about any non-standard types.
               
               if (not (EntryType.lower().strip() in ExpectedTypes)) :
                  Problem = "Unexpected .bib file entry '" + EntryType + \
                                                 "' - will default to 'MISC'"
                  if (not BatchMode) : print "*",Problem,"*"
                  State = States.NEED_AT
      
         else :
         
            #  If we need a brace, look for it and if we have one, we then
            #  want the reference and its terminating comma - we assume these
            #  will be on the same line. Then we will probably find the comma
            #  in the next block. If not, on the next line.

            if (State == States.NEED_BRACE) :
               Brace = BibFileLine.find('{')
               if (Brace >= 0) :
                  BibFileLine = BibFileLine[Brace + 1:]
                  State = States.NEED_COMMA

            #  If we're looking for the reference name itself followed by
            #  a comma, see if we have that. This does assume the comma is
            #  on the same line as the name (how many odd formats are we
            #  trying to handle?)

            if (State == States.NEED_COMMA) :
               BibFileLine = BibFileLine.lstrip()
               Comma = BibFileLine.find(",")
               if (Comma > 0) :
                  Ref = BibFileLine[:Comma].strip()
                  State = States.NEED_AT
                  BibFileRefs.append(Ref)
         
      BibFile.close()
   else:
      if (not BatchMode) : print "**No bib file called",BibFileName,"found**"
      
   return BibFileRefs

# ------------------------------------------------------------------------------

#                        G e t  T e x  F i l e  R e f s
#
#   Looks in the current directory for the specified .tex file, and
#   adds the identifiers of all the references it cites to the list
#   passed as TexFileRefs, and adds any bibitems it finds to the list
#   passed as BibItemRefs. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.

def GetTexFileRefs (TexFileName,TexFileRefs,BibItemRefs,Problems = None):

   TexFile = open(TexFileName,mode='r')
   TheScanner = TexScanner.TexScanner()
   TheScanner.SetFile(TexFile)

   #  GetNextTexCommand() will call RefsScanCallback for each command it
   #  finds in the file, and RefsScanCallback will check the command
   #  and add any cited references to TexFileRefs and any items defined
   #  using \bibitem to BibItemRefs.

   Finished = False
   Refs = (TexFileRefs,BibItemRefs)
   while (not Finished) :
      Finished = TheScanner.GetNextTexCommand(RefsScanCallback,Refs,Problems)

   TexFile.close()

# ------------------------------------------------------------------------------

#                        F i n d  B i b  F i l e
#
#   Looks in the current directory for the .bib file associated with the
#   specified paper. This should either be the standard .bib file used by
#   all the papers when in their final form, as returned by GetBibFileName(),
#   or it should have the same name as the main paper but with a .bib
#   extension, eg O1-3.bib. This routine looks first for the standard .bib
#   file, and if cannot find that, looks for the one with the same name as
#   the paper. It returns the first of these that it finds. If neither
#   exists, it looks for any .bib file in the directory. If it finds none, it
#   returns blank.
#
#   Note that it is possible that the .tex file is using a .bib file with
#   neither of these names, eg with a \bibliography{example} directive. This
#   routine could check for that, but at the moment it doesn't.
#
#   The optional Details parameter can be a list of strings to which this
#   routine will append a description of the file it is using.

def FindBibFile (Paper,Details = None) :

   BatchMode = False
   if (Details != None) : BatchMode = True
   
   Found = False
   BibFileName = GetBibFileName()
   if (BibFileName != "") : Found = os.path.exists(BibFileName)
   if (Found) :
      Report = "Using standard .bib file " + BibFileName
      if (BatchMode) :
         Details.append(Report)
      else :
         print Report
   else :
      BibFileName = Paper + ".bib"
      Found = os.path.exists(BibFileName)
      if (Found) :
         Report = "Using .bib file " + BibFileName + " (based on paper name)"
         if (BatchMode) :
            Details.append(Report)
         else :
            print Report
      else :
         BibFileCount = 0
         FileList = os.listdir(".")
         for File in FileList :
            if (File.endswith(".bib")) :
               if (BibFileCount == 0) : BibFileName = File
               BibFileCount = BibFileCount + 1
               Found = True
         if (Found) :
            Report = "Using .bib file " + BibFileName
            if (BibFileCount > 1) :
               Report = Report + " (first of " + str(BibFileCount) + \
                                                   " .bib files found)"
            if (BatchMode) :
               Details.append(Report)
            else :
               print Report
   if (not Found) : BibFileName = ""

   return BibFileName

# ------------------------------------------------------------------------------

#                            V e r i f y  R e f s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper, and also looks for the
#   file called "adass<conf>references.bib" which it assumes contains the
#   BibTeX references for the paper. If this file cannot be found, it will
#   check for a file called Paper.bib. It checks that all the references in
#   the .bib file are used by the .tex file, and that all the references
#   used by the .tex file are defined in the .bib file (or, being tolerant,
#   defined using \bibitem directives in the .tex file, although it warns
#   about these). It lists all the references, so the user can see what
#   (if any) naming convention is being used.
#
#   The optional arguments allow this to be used with the PaperCheck
#   initial verification code, where the paper name and the bib file name
#   may not be the standard names expected, and allow control over whether
#   or not we allow the use of \bibitem entries or not. It also now returns
#   True if no problems were found, False otherwise. The final optional
#   Problems and Warnings arguments allow this to be used in batch mode, where
#   direct output from this routine is suppressed and instead a set of report
#   lines are added to the list of problems passed.

def VerifyRefs (Paper,AllowBibitems = True,TexFileName = "",BibFileName = "", \
                                            Problems = None, Warnings = None) :

   ReturnOK = True
   
   BatchMode = False
   if (Problems != None and Warnings != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print Problem
      ReturnOK = False
   else :

      #  Assume that the .bib file to use (if any) has the same name as
      #  the common reference .bib file. Get a list of all the references it
      #  contains so we can see what soft of naming convention is used,
      #  and so we can check them against the references in the .tex file.

      LookForBibFile = False
      if (BibFileName == "") :
         LookForBibFile = True
      else :
         if (not os.path.exists(BibFileName)) : LookForBibFile = True
      if (LookForBibFile) : BibFileName = FindBibFile(Paper)

      if (BibFileName == "") :
         BibFileRefs = []
      else :
         BibFileRefs = GetBibFileRefs(BibFileName,BatchMode)
         if (not BatchMode) :
            print ""
            print "References in",BibFileName," :"
            for BibRef in BibFileRefs :
               print "   ",BibRef
            print ""

      #  The .bib file name we've ended up with may not be the one specified
      #  in the .tex file, and we check for that.

      if (not BatchMode) :
         Warn = False
         TexFile = open(TexFileName,mode='r')
         for TexFileLine in TexFile :
            if (not TexFileLine.startswith("%")) :
               if (TexFileLine.find("\\usepackage{./asp2014}") >= 0) :
                  print "** .tex file has \\usepackage{./asp2014} directive **"
                  Warn = True
               Index = TexFileLine.find("\\bibliography{")
               if (Index >= 0) :
                  Right = TexFileLine[Index:].find("}")
                  if (Right > 0) :
                     OldBib = TexFileLine[Index:Index + Right + 1]
                     BibFileBase = os.path.splitext(BibFileName)[0]
                     if (OldBib != "\\bibliography{" + BibFileBase + "}" and \
                          OldBib != "\\bibliography{" + BibFileName + "}") :
                        print "** Note: Tex file includes",OldBib,"directive **"
                        Warn = True
         TexFile.close()
         if (Warn) :
            print "** .tex file directives may need correcting **"
            ReturnOK = False

      #  Now get a list of the \citet and \citep commands in the .tex file
      #  We also see if there are any \bibitem definitions, although people
      #  aren't supposed to be using these.

      TexFileRefs = []
      BibItemRefs = []

      GetTexFileRefs(TexFileName,TexFileRefs,BibItemRefs,Problems)

      if (not BatchMode) :
         if (len(TexFileRefs) > 0) :
            print "References cited in",TexFileName,":"
            for TexRef in TexFileRefs :
               print "   ",TexRef.strip()
            print " "
      BibItemCount = len(BibItemRefs)
      if (BibItemCount > 0) :
         if (BatchMode) :
            if (not AllowBibitems) :
               Problems.append( \
                        "Tex file has the following \\bibitem directives:")
               for BibItem in BibItemRefs :
                  Problems.append(BibItem.strip())
         else :
            print "** Note: Tex file has",BibItemCount,"\\bibitem directives **"
            for BibItem in BibItemRefs :
               print "    ",BibItem.strip()
            if (not AllowBibitems) :
               ReturnOK = False
               print "** These need to be replaced by a .bib file", \
                                                     "with BibTex entries **"

      #  See if all the references defined in the .bib file are used
      #  in the .tex file.

      if (len(BibFileRefs) == 0) :
         if (not BatchMode) : print "No Bib file references supplied"
      else :
         AllUsed = True
         for BibRef in BibFileRefs :
            BibRef = BibRef.strip()
            BibRefLower = BibRef.lower()
            Found = False
            CaseCheck = False
            for TexRef in TexFileRefs :
               TexRef = TexRef.strip()
               if (BibRef == TexRef) :
                  Found = True
                  CaseCheck = True
                  break
               if (BibRefLower == TexRef.lower()) :
                  Found = True
                  break
            if (not Found) :
               Warning = "Bib file reference " + BibRef + \
                                                    " not used in .tex file"
               if (BatchMode) : Warnings.append(Warning)
               else : print Warning
               AllUsed = False
            if (Found and (not CaseCheck)) :
               Problem = "Bib file reference " + BibRef + \
                                   " used with different case in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print Problem
         if (AllUsed) :
            if (not BatchMode) :
               print "All Bib file references used in .tex file"
         else :
            ReturnOK = False

      #  And the same for the \bibitem definitions - not that we approve -
      #  if there were any.

      if (BibItemCount > 0) :
         AllUsed = True
         for BibItem in BibItemRefs :
            BibItem = BibItem.strip()
            Found = False
            for TexRef in TexFileRefs :
               TexRef = TexRef.strip()
               if (BibItem == TexRef) :
                  Found = True
                  break
            if (not Found) :
               Problem = "\\bibitem reference " + BibItem + \
                                             " not used in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print Problem
               AllUsed = False
         if (AllUsed) :
            if (not BatchMode) :
               print "All \\bibitem references used in .tex file"
         else :
            ReturnOK = False

      #  See if all the references cited in the .tex file are defined
      #  in the .bib file or at least in the \bibitem definitions (not 
      #  that we approve of those).

      if (len(TexFileRefs) == 0) :
         if (not BatchMode) : print "No citations found in tex file"
      else :
         AllFound = True
         for TexRef in TexFileRefs :
            TexRef = TexRef.strip()
            TexRefLower = TexRef.lower()
            Found = False
            AsBibitem = False
            CaseCheck = False
            for BibRef in BibFileRefs :
               BibRef = BibRef.strip()
               if (TexRef == BibRef) :
                  Found = True
                  CaseCheck = True
                  break
               if (TexRefLower == BibRef.lower()) :
                  Found = True
                  break
            if (not Found) :
               for BibItem in BibItemRefs :
                  BibItem = BibItem.strip()
                  if (TexRef == BibItem) :
                     Found = True
                     CaseCheck = True
                     AsBibitem = True
                     break
                  if (TexRefLower == BibItem.lower()) :
                     Found = True
                     AsBibItem = True
                     break
            if (not Found) :
               Problem = ".tex file reference " + TexRef + " undefined"
               if (BatchMode) : Problems.append(Problem)
               else : print Problem
               AllFound = False
            if (Found and (not CaseCheck)) :
               Problem = ".tex file reference " + TexRef + \
                                     " defined but with different case"
               if (BatchMode) : Problems.append(Problem)
               else : print Problem
            if (Found and AsBibitem and not AllowBibitems) :
               Problem = ".tex file reference " + TexRef + \
                                     " defined but as a \\bibitem entry"
               if (BatchMode) : Problems.append(Problem)
               else : print Problem
      
         if (AllFound) :
            if (not BatchMode) : print "All .tex file citations defined"
         else :
            ReturnOK = False
         
   print ""
   
   return ReturnOK
   
# ------------------------------------------------------------------------------

#                       R e f  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for citations to references that should be in the .bib
#   file. Also scans for references defined within the .tex file using
#   \bibitem entries. Words are the components of a LaTeX directive parsed 
#   by the TexScanner. The second argument, Refs, should be a list of two
#   lists, the first being TexFileRefs (a list of cited references in the file)
#   and the second being BibItemRefs (a list of any \bibitem entries in the
#   file - which we don't approve of, but need to know about). If this is a
#   recognised citation, the cited references are added to TexFileRefs. If it
#   is a \bibitem entry, the name of the reference is added to BibItemRefs.
#   TexFileRefs and BibItemRefs are both lists of strings. The final optional
#   Problems argument allows this to be used in batch mode, where direct output
#   from this routine is suppressed and instead a set of report lines are added
#   to the list of problems passed.

def RefsScanCallback (Words,Refs,Problems = None) :
   
   TexFileRefs = Refs[0]
   BibItemRefs = Refs[1]
   
   BatchMode = (Problems != None)

   if (len(Words) > 0) :
   
      #  See if we have "\cite" or "\Cite". If so, this is should be one of the
      #  citation options provided by the natbib package. This provides a
      #  large number of options - see 
      #  http://texdoc.net/texmf-dist/doc/latex/natbib/natbib.pdf
      #  and this code checks for all of them, splitting things into the
      #  options that start with "\cite" and those that start with "\Cite".
      #  All of these commands take a non-optional argument that is one or
      #  more references that should be defined in a .bib file (or perhaps
      #  using \bibitem entries). The "\cite" command is expressly warned
      #  about in the natbib documentation, and ADASS doesn't allow it, so
      #  it's trapped here. The only legitimate natbib option not included
      #  here is "\citetext" which does not take a reference argument - it
      #  takes literal text - and this will end up generating a warning.
      
      if (Words[0][:5].lower() == "\\cite") :
         Match = False
         Refs = ExtractRefs(Words)
         if (Words[0][1] == 'c') :
         
            #  Check the upper case options \citexxx
            
            if (len(Words[0]) == 5) :
               Problem = "Note use of \cite for reference '" + Refs + \
                                                        "' in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print "**",Problem,"**"
               Match = True
            else :
               LowerCaseOptions = ["t","p","t*","p*","alt","alt*","alp","alp*",\
                         "num","author","author*","year","yearpar","fullauthor"]
               Option = Words[0][5:]
               for Opt in LowerCaseOptions :
                  if (Option == Opt) :
                     Match = True
                     break
         else :
         
            #  Check the upper case options \Citexxx
            
            if (len(Words[0]) > 5) :
               UpperCaseOptions = ["t","p","t*","p*","alt","alt*","alp","alp*",\
                                                             "author","author*"]
               Option = Words[0][5:]
               for Opt in UpperCaseOptions :
                  if (Option == Opt) :
                     Match = True
                     break
         if (not Match) :
            Problem = "Note: use of " + ' '.join(Words) + " in .tex file"
            if (BatchMode) : Problems.append(Problem)
            else : print "**",Problem,"**"
         else :
         
            #  If we found one of the \cite commands, get the references from
            #  its arguments.
            
            if (Refs != "") :
               RefList = Refs.split(",")
               TexFileRefs.extend(RefList)
            else :
               Problem = "Note: no reference list in " + ' '.join(Words) + \
                                                            " in .tex file"
               if (BatchMode) : Problems.append(Problem)
               else : print "**",Problem,"**"

      #  Finally, pick up any \bibitem entries, while we're at it.
      
      if (Words[0] == "\\bibitem") :
         Refs = ExtractRefs(Words)
         if (Refs != "") :
            BibItemRefs.append(Refs.strip("{}"))
         else :
            Problem = "Note: no reference list in " + ' '.join(Words) + \
                                                            "in .tex file"
            if (BatchMode) : Problems.append(Problem)
            else : print "**",Problem,"**"

# ------------------------------------------------------------------------------

#                            V e r i f y  E p s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any plotting
#   commands (\plotone, \plottwo, \plotfiddle, or \includegraphics, which
#   should cover all the commands used in ADASS papers) and collects the
#   names of the files used by these commands. It then looks at the files
#   in the current directory and checks that all of them are present, and
#   also checks that there are no additional .eps files that are unused.
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument. The final optional Problems and Warnings arguments
#   allow this to be used in batch mode, where direct output from this routine
#   is suppressed and instead a set of report lines are added to the lists of
#   problems and warnings passed.
#
#   This routine returns True if everything looks OK, False otherwise.


def VerifyEps (Paper,TexFileName = "",Problems = None,Warnings = None) :

   #  CalledFromWalk() is the function passed to os.path.walk() in order
   #  to build up a full list of the files in the current directory. Each file
   #  found is added to FileList. We strip off any leading './' as this is
   #  (we assume) not going to be included when the .tex file refers to the
   #  file.
   
   def CalledFromWalk(FileList,DirPath,Namelist) :
      if (DirPath.find("__MACOSX") < 0) :
         for Name in Namelist :
            Path = os.path.join(DirPath,Name)
            if (Path.startswith("./")) : Path = Path[2:]
            FileList.append(Path)
   
   ReturnOK = True
   
   BatchMode = False
   if (Problems != None and Warnings != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print "**",Problem,"**"
      ReturnOK = False
   else :

      #  Now get a list of the files used by the graphics commands in the .tex
      #  file.

      FileListFromTex = []
      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call EpsScanCallback for each command it
      #  finds in the file, and EpsScanCallback will check the command
      #  and add any specified graphic file names used to FileListFromTex.
      
      Finished = False
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(EpsScanCallback,\
                                                      FileListFromTex,None)
                                                         
      TexFile.close()

      #  See if any of the graphics files are in sub-directories. They shouldn't
      #  be, but people often do put them there.
      
      DirListFromTex = []
      for FileName in FileListFromTex :
         DirName = os.path.dirname(FileName)
         if (DirName != "") :
            if (not (DirName in DirListFromTex)) :
               DirListFromTex.append(DirName)

      #  Get a list of all the files in the directory and its subdirectories.
      #  (os.path.walk() calls CalledFromWalk() for each directory found, and
      #  CalledFromWalk() - defined above - adds the paths for all files
      #  - minus any leading './' - to FileList.)
      
      FileList = []
      os.path.walk('.',CalledFromWalk,FileList)

      #  First, simply list all the graphics files specified by the .tex file.
      
      if (len(FileListFromTex) > 0) :
         if (not BatchMode) :
            print "Graphics files used by",TexFileName,":"
            for FileName in FileListFromTex :
               print "    ",FileName
         if (len(DirListFromTex) > 0) :
            Problem = "Some graphics files are in sub-directories"
            if (BatchMode) : Problems.append(Problem)
            else : print "**",Problem,"**"
         
         #  Now run through them again, checking for files with .eps extensions.
         #  If so, see if they were supplied. 
         
         for FileName in FileListFromTex :
            if (not FileName.endswith(".eps")) :
            
               #  It didn't end with .eps. See what it did end with.
               
               Ext = os.path.splitext(FileName)[1]
               if (Ext == "") :
               
                  #  Here, the .tex file did not specify an extension. It will
                  #  default to any graphics file in the directory, which may
                  #  or may not be a .eps file. There are a number of tricky
                  #  possibilities here.
                  
                  MatchedFiles = []
                  EpsMatch = False
                  for File in FileList :
                     if (File.startswith(FileName + '.')) :
                        MatchedFiles.append(File)
                        if (os.path.splitext(File)[1] == ".eps") :
                           EpsMatch = True
                  if (len(MatchedFiles) != 1) : ReturnOK = False;
                  if (len(MatchedFiles) > 1) :
                     Problem = FileName + " may default to any of:"
                     if (BatchMode) : Problems.append(Problem)
                     else : print "**",Problem,"**"
                     Files = ""
                     for Match in MatchedFiles :
                        Files = Files + Match + " "
                     if (BatchMode) : Problems.append(Files)
                     else : print "    ",Files
                     if (EpsMatch) :
                        Problem = "Only one of which is an eps file"
                     else :
                        Problem = "None of which seem to be suitable"
                        if (BatchMode) : Problems.append(Problem)
                        else : print "**",Problem,"**"
                  elif (len(MatchedFiles) == 1) :
                     if (EpsMatch) :
                        Note = "(Note: " + FileName + \
                                                      " will default to .eps )"
                        if (not BatchMode) : print Note
                     else :
                        Problem = FileName + \
                         " will default to the non-eps file " + MatchedFiles[0]
                        ReturnOK = False
                        if (BatchMode) : Problems.append(Problem)
                        else : print "**",Problem,"**"
                  else :
                     Problem = "No files match " + FileName
                     if (BatchMode) : Problems.append(Problem)
                     else : print "**",Problem,"**"

               else :
               
                  #  A non-eps extension needs to be noted. See if the
                  #  file exists and if not warn about that as well.
                  
                  Problem = FileName + " does not have a .eps extension"
                  if (BatchMode) : Problems.append(Problem)
                  else : print "**",Problem,"**"
                  if (not os.path.exists(FileName)) :
                     Problem = FileName + " has not been supplied"
                     if (BatchMode) : Problems.append(Problem)
                     else : print "**",Problem,"**"
                  ReturnOK = False
                     
         print " "
      
      #  List all the .eps files in the current directory.
      
      EpsFileList = []
      for File in FileList :
         if (not File.startswith('.')) :
            if (File.endswith(".eps")) : EpsFileList.append(File)
      if (not BatchMode) :
         print ".eps files supplied:"
         if (len(EpsFileList) > 0) :
            for FileName in EpsFileList :
               print "    ",FileName.strip()
            print " "
      
      #  See if all the .eps files are used by the .tex file.
      
      if (len(EpsFileList) == 0) :
         if (not BatchMode) : print "No .eps files found"
      else :
         AllFound = True
         for EpsFile in EpsFileList :
            Found = False
            for GraphicsFile in FileListFromTex :
               if (GraphicsFile == EpsFile) :
                  Found = True
                  break
               if (GraphicsFile.lower() == EpsFile.lower()) :
                  Found = True
                  CaseProblems = True
                  Problem = GraphicsFile + " matches " + EpsFile + \
                                                       " but has different case"
                  if (BatchMode) : Problems.append(Problem)
                  else : print "**",Problem,"**"
                  break
               if (GraphicsFile.find('.') < 0) :
                  if (GraphicsFile + ".eps" == EpsFile) :
                     Found = True
                     break
                  if (GraphicsFile.lower() + ".eps" == EpsFile.lower()) :
                     Found = True
                     CaseProblems = True
                     Problem = GraphicsFile + " matches " + EpsFile + \
                                                      " but has different case"
                     if (BatchMode) : Problems.append(Problem)
                     else : print "**",Problem,"**"
                     break
            if (not Found) :
               Warning = EpsFile + " is not used in the .tex file"
               if (BatchMode) : Warnings.append(Warning)
               else : print "*",Warning,"*"
               AllFound = False
         if (AllFound) :
            if (not BatchMode) :
               print "All .eps files in the directory are used by the .tex file"
         else :
            ReturnOK = False
      
      #  See if all the files used by the .tex file are in the directory.
      #  At this point, we assume that if no extension was specified, it
      #  will default to .eps. Note that if we are running on a file system that
      #  is case-insensitive (eg OS X in most cases), you can get away with case
      #  errors in the file names that will cause problems on other systems.
      #  File names should match properly, but we don't want to flag a file as
      #  missing just because of a case error.
      
      if (len(FileListFromTex) == 0) :
         if (not BatchMode) : print "No graphics files used by the .tex file"
      else :
         AllFound = True
         AllEps = True
         CaseProblems = False
         for GraphicsFile in FileListFromTex :
            if (os.path.splitext(GraphicsFile)[1] == "") :
               GraphicsFile = GraphicsFile + ".eps"
            Found = False
            for EpsFile in EpsFileList :
               if (EpsFile == GraphicsFile) :
                  Found = True
                  break
               if (EpsFile.lower() == GraphicsFile.lower()) :
                  Found = True
                  CaseProblems = True
                  Problem = EpsFile + " matches " + GraphicsFile + \
                                                       " but has different case"
                  if (BatchMode) : Problems.append(Problem)
                  else : print "**",Problem,"**"
                  break
            if (not Found) :
               for File in FileList :
                  if (File == GraphicsFile) :
                     Found = True
                     AllEps = False
                     break
                  if (File.lower() == GraphicsFile.lower()) :
                     Found = True
                     AllEps = False
                     CaseProblems = True
                     Problem = File + " matches " + GraphicsFile + \
                                                       " but has different case"
                     if (BatchMode) : Problems.append(Problem)
                     else : print "**",Problem,"**"
                     break
            if (not Found) :
               Problem = GraphicsFile + " is missing from the directory"
               if (BatchMode) : Problems.append(Problem)
               else : print "**",Problem,"**"
               AllFound = False
               ReturnOK = False
         if (AllFound) :
            if (not BatchMode) :
               print "All graphics files used by the .tex file are supplied"
            if (not AllEps) :
               Problem = "Not all graphics files are .eps files"
               if (BatchMode) : Problems.append(Problem)
               else : print "**",Problem,"**"
               ReturnOK = False
            if (len(DirListFromTex) > 0) :
               Problem = "Graphics files should not be in subdirectories"
               if (BatchMode) : Problems.append(Problem)
               else : print "**",Problem,"**"
               ReturnOK = False

         if (CaseProblems) :
            Problem = \
                 "Some graphics files names have problems with upper/lower case"
            if (BatchMode) : Problems.append(Problem)
            else : print "**",Problem,"**"
            ReturnOK = False

   return ReturnOK
               
# ------------------------------------------------------------------------------

#                       E p s  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for references to figures that should be supplied in files.
#   Words are the components of a LaTeX directive parsed by the TexScanner. If
#   this is a recognised graphics command, the specified file name will be
#   added to FileListFromTex, which is a list of strings. TexScanner supplies
#   an additional argument when it makes the callback, but this is unused here.
#   File names already in the list are not added to it - some .tex files use
#   the same image more than once. Any leading "./" characters are removed from
#   the file names; I don't think they should really be there, but this makes
#   things consistent with the way the files found in the directory are handled
#   when the two are compared by VerifyEps().

def EpsScanCallback (Words,FileListFromTex,Unused) :
   if (len(Words) > 0) :
      if (Words[0] == "\\includegraphics" or \
            Words[0] == "\\articlefigure" or \
               Words[0] == "\\articlefiguretwo" or \
                  Words[0] == "\\articlefigurethree" or \
                     Words[0] == "\\articlefigurefour" or \
                        Words[0] == "\\articlelandscapefigure" or \
                           Words[0] == "\\articlelandscapefiguretwo" or \
                              Words[0] == "\\plotone" or \
                                 Words[0] == "\\plottwo" or \
                                    Words[0] == "\\plotfiddle") :
         FileCount = 0
         MaxFiles = 1
         if (Words[0].find("two") > 0) : MaxFiles = 2;
         if (Words[0].find("three") > 0) : MaxFiles = 3;
         if (Words[0].find("four") > 0) : MaxFiles = 4;
         for Word in Words[1:] :
            if (Word != "") :
               if (Word[0] == '{') :
                  FileCount = FileCount + 1
                  File = Word.strip("{}")
                  if (File.startswith("./")) : File = File[2:]
                  File = File.strip()
                  if (not File in FileListFromTex) :
                     FileListFromTex.append(File)
                  if (FileCount >= MaxFiles) : break
                  
# ------------------------------------------------------------------------------

#                        T r i m  B i b  F i l e
#
#  A rather crude utility that comments out any references defined in the
#  adass conference .bib file in the default directory that are unused by
#  the main .tex file for the specified paper in the same default directory.
#  The unused entries can be either commented out or deleted entirely, 
#  depending on the Keep argument.
#
#  Note that BibTeX has unusual commenting arrangements. Strictly, it does 
#  not recognise '%' as introducing a comment, but rather treats anything
#  not included in a reference (introduced by a line with an @) as a comment.
#  So you can't comment out a line within a reference by starting it with '%'.
#  More unusually, if a line starts, for example, '%@inproceedings' it treats
#  the % as a comment outside the reference block, which it assumes starts 
#  with the @inproceedings. So this program puts % characters at the start
#  of each commented out block, as this makes it stand out in most LaTeX-aware
#  editors, which can be useful, but it also replaces that crucial '@'
#  with '_AT_' (which strictly is all that it needs to do).
#
#  Really, of course, there's no need to comment out the unused items, once
#  we can be confident the program works properly - they could just be
#  deleted entirely, and that's an option here that can triggered by setting
#  the Keep argument false.

def TrimBibFile (Paper,Keep = True) :

   BibFileName = FindBibFile(Paper)
   BibFileRefs = GetBibFileRefs(BibFileName)
   print ""
   print "References in",BibFileName," :"
   for BibRef in BibFileRefs :
      print "   ",BibRef
   print ""
   
   if (len(BibFileRefs) > 0) :
   
      TexFileRefs = []
      BibItemRefs = []
      
      ParsedOK = True
   
      TexFileName = os.path.abspath(Paper + ".tex")
      if (not os.path.exists(TexFileName)) :
         print "Cannot find main .tex file",TexFileName
      else :
   
         GetTexFileRefs (TexFileName,TexFileRefs,BibItemRefs)
         
         BibFile = open(BibFileName,mode='r')
         ModBibFileName = "oldReferences.bib"
         ModBibFile = open(ModBibFileName,mode='w')
         Changed = False
         CommentingOut = False
         BraceCount = 0
         LineCount = 0
         for BibFileLine in BibFile :
         
            #  The parsing here is rather crude. It assumes that each
            #  starts with a line that begins "@type{name" and goes on
            #  to count '{' and '}' characters and assumes the entry 
            #  ends when these are balanced. There may be files that
            #  break this, but most should be OK.
            
            LineCount = LineCount + 1
            ThisIsAComment = False
            if (not BibFileLine.strip().startswith('%')) :
               if (CommentingOut) :
                  BraceCount = BraceCount + BibFileLine.count('{') - \
                                              BibFileLine.count('}')
                  if (BraceCount <= 0) :
                     CommentingOut = False
                     BraceCount = 0
                  BibFileLine = '%' + BibFileLine
                  ThisIsAComment = True
               else :
                  if (BibFileLine.strip().startswith("@")) :
                  
                     #  Lines starting with '@' indicate a new reference.
                     #  Extract the name, then see if this is one that's in
                     #  the list of those used by the .tex file. This 
                     #  parsing has problems with cases where the name is on
                     #  the next line. Handling this is tricky, as we don't
                     #  know if we want to keep the reference until we've read
                     #  the second line. For the moment, we just flag the
                     #  problem and keep the reference.
                     
                     Brace = BibFileLine.find("{")
                     if (Brace > 0) :
                        Comma = BibFileLine.find(",")
                        if (Comma > 0) :
                           Ref = BibFileLine[Brace + 1:Comma]
                        else :
                           Ref = BibFileLine[Brace + 1:]
                        Ref = Ref.strip()
                        Used = False
                        if (Ref == "") :
                           print "** Blank name in .bib file at line",\
                                                              LineCount,"**"
                           ParsedOK = False
                           Used = True
                        for TexFileRef in TexFileRefs :
                           if (Ref == TexFileRef.strip()) :
                              Used = True
                              print "Keeping reference",Ref
                              break
                        if (not Used) :
                           BibFileLine = '%' + BibFileLine.replace('@',"_AT_")
                           print "Commenting out unused reference",Ref
                           Changed = True
                           CommentingOut = True
                           ThisIsAComment = True
                           BraceCount = BibFileLine.count('{') - \
                                              BibFileLine.count('}')
            WriteThis = True
            if (ThisIsAComment and (not Keep)) : WriteThis = False
            if (WriteThis) : ModBibFile.write(BibFileLine)
         ModBibFile.close()
         BibFile.close()
         
         if (Changed) :
            os.rename(BibFileName,BibFileName + ".old")
            os.rename(ModBibFileName,BibFileName)
         else :
            os.unlink(ModBibFileName)
            
         if (not ParsedOK) :
            print ""
            print "** Problem parsing the file may mean an unused reference"
            print "has been kept. Suggest running RefCheck and editing the"
            print "file to fix the parsing problem if necessary **"

# ------------------------------------------------------------------------------

#                           G e t  I n i t i a l
#
#  Given a forename, and an index into it (which will usually be 0, but
#  might be more if there is hyphenation involved), returns the initial letter
#  at that index position in the forename. Usually, this will just be the
#  character at Forename[Index], but this allows for initials using one of 
#  the special character sequences of the form "\x{c}" such as \c{c} for a 
#  c-cedilla. Notes is a list to which any message may be appended.
 
def GetInitial (Forename,Index,Notes) :
   Initial = Forename[Index]
   Letter = Initial
   if (Initial == '\\') :
      Initial = '?'
      Len = len(Forename)
      if (len(Forename) > Index + 4) :
         if (Forename[Index + 2] == '{' and Forename[Index + 4] == '}') :
            Initial = Forename[Index:Index + 5]
            Letter = Forename[Index + 3]
   if (Initial == '?') :
      Note = "Unexpected control sequence for initial in " + Forename
      Notes.append(Note)
   else :
      if (Letter.islower()) :
         Note = "Initial letter in '" + Forename + "' is in lower case"
         Notes.append(Note)
            
   return Initial
            
# ------------------------------------------------------------------------------

#                       A u t h o r  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for an author list. Words are the components of a LaTeX
#   directive parsed by the TexScanner. If this is the list of authors in
#   the paper (the \author directive) this parses the arguments to that
#   directive and adds to the supplied AuthorList argument one string for
#   each author, formatted in the <Surname><Initials> format required - eg
#   "Shortridge,~K." Notes should be a list to which this will append strings
#   briefly describing any possible problems the routine has spotted while
#   processing the author list. If there are any such notes, the raw author
#   list will be appended as a final note.
#
#   (This originally quite simple code got messier and messier as more and
#   more edge cases - hyphenated names, accented names, suffixes like Jr.,
#   van der This and von That, etc. - turned up and were handled. It really
#   would benefit from a redesign, but it seems to work fairly well now, so
#   long as you have a good look at what it produces and don't trust it
#   implicitly to get every name perfect. At the moment, the main ones I've
#   seen that it gets wrong are a) cases such as 'An Author, for the rest of
#   the team', which really don't fit the standard format, and b) Spanish names
#   where the surname is two separate names, not hyphenated, where there really
#   is no obvious way to tell if a 'middle' name is a forename or part of the
#   surname. Think Mario Vargas Llosa. At least both these cases are picked up
#   by the code and reported in Notes.)
#   

def AuthorScanCallback(Words,AuthorList,Notes) :

   if (len(Words) > 1) :
      if (Words[0] == "\\author") :
         Authors = Words[1].strip()
         Len = len(Authors)
         if (Len > 0) :
            if (Authors.startswith('{')) :
            
               #  Trim down to just the list of authors. Lose the leading '{'
               #  and then anything following \affil. There ought to be an
               #  \affil, but if there isn't, lose the trailing '}'.
               
               EndIndex = Authors.find("\\affil")
               if (EndIndex < 0) :
                  EndIndex = Authors.rfind('}')
               if (EndIndex <= 0) :
                  Notes.append("Misformed author list")
               else :
                  Authors = Authors[1:EndIndex]
                  
                  #  For our purposes, "\ " is just a space. And we aren't 
                  #  interested in forced line breaks - "\\" or "\\*". (It's
                  #  important to do these in the right order!)
                  
                  Authors = Authors.replace("\\\\*",'')
                  Authors = Authors.replace("\\\\",'')
                  Authors = Authors.replace("\\ ",' ')
                  
                  #  If we have any issues, it helps to report the author
                  #  list in as raw a form as possible. What we have at this 
                  #  point will probably do.
                  
                  RawAuthors = Authors
                  
                  #  Some constructs involving a space are confusing. If
                  #  anyone has set c-cedilla as '\c c' we replace it with
                  #  the equivalent '\c{c}'. There are others.
                  
                  Accents = "`'^\"H~ckl=b.druv"
                  for Char in Accents :
                     More = True
                     while (More) :
                        Index = Authors.find('\\'+Char+' ')
                        if (Index >= 0) :
                           Cposn = Index + 3
                           if (Cposn < len(Authors)) :
                              Str = '\\'+Char+' '+Authors[Cposn]
                              Repl = '\\'+Char+'{'+Authors[Cposn]+'}'
                              Authors = Authors.replace(Str,Repl)
                        else :
                           More = False
                                                
                  #  We should now have a comma-separated author list.
                  #  Lose anything in math (between $signs$) because these
                  #  will be the affiliation superscripts (and if they contain
                  #  commas, eg "$^{1,2}$" this confuses the splitting into
                  #  individual names). We replace any math expression by a 
                  #  single space, so that it acts as a separator. We only 
                  #  expect one math expression per author - more may be
                  #  an indication of a missing comma.
                  #
                  #  Replacing the math expression with a comma instead of a
                  #  space would allow us to get the index entries right, but
                  #  might confuse the comma count, including the check for
                  #  a missing serial comma, and that's not a good thing.
                  
                  Authors = Authors.strip()
                  Len = len(Authors)
                  InMath = False
                  AString = ""
                  MathCount = 0
                  Posn = 0
                  for Index in range(Len) :
                     Char = Authors[Index]
                     if (Char == '$') :
                        if (InMath) :
                           InMath = False
                           if (MathCount > 0 and Index < (Len - 1)) :
                              Notes.append("Possible missing comma near '" + \
                                               Authors[Posn:Index] + "'")
                           MathCount = MathCount + 1
                           Posn = Index
                        else :
                           InMath = True
                           AString = AString + ' '
                     else :
                        if (not InMath) :
                           if (Char == ',') : MathCount = 0 
                           AString = AString + Char
                        
                  #  The exception to the rule that all names are separated
                  #  by commas is the two author case, where they are separated
                  #  by 'and'. Trap that case and insert the comma to make
                  #  the split work properly.
                  
                  if (AString.find(',') < 0) :
                     AndIndex = AString.find(" and ")
                     if (AndIndex > 0) :
                        AString = AString[:AndIndex] + ',' + \
                                              AString[AndIndex:]
                  
                  #  And I've seen people get carried away with commas at the
                  #  end of the each author in the list.
                  
                  AString = AString.strip()
                  Len = len(AString)
                  if (Len > 0) :                       
                     if (AString[Len - 1] == ',') :
                        Note = "Extraneous comma at end of author list"
                        Notes.append(Note)
                        AString = AString[:Len - 1]
                  
                  #  Split the string as we have it now into what we hope 
                  #  are the individual name sections - the bits separated
                  #  by commas.
                            
                  AList = AString.split(",")
                  
                  #  Missing out the final serial comma is a common mistake
                  #  in multi-author lists. It's worth going to the trouble
                  #  of checking for that and pointing it out. If we find
                  #  the last 'author' has an 'and' other than at the start,
                  #  we replace it with a comma and redo the splitting.
                  
                  NAuthors = len(AList)
                  if (NAuthors > 0) :
                     Author = AList[NAuthors - 1]
                     if (Author == "") :
                        if (NAuthors > 1) : Author = AList[NAuthors - 2]
                     Author = Author.replace('~',' ').replace('.',' ').strip()
                     if ( not Author.startswith("and")) :
                        if (Author.find(" and ") >= 0) :
                           Note = "Note: '" + Author + \
                                           "' may have a missing serial comma."
                           Notes.append(Note)
                           AString = AString.replace(" and ",',')
                           AList = AString.split(",")
                  
                  #  Now go through all of what should be individual authors.
                  
                  OrderWarning = False
                  Len = len(AList)
                  for Index in range(Len) :
                  
                     Author = AList[Index]
                  
                     #  '~' and '.' characters just confuse things. We want the
                     #  individual names (or initials, we don't care which).
                     #  So "Yet Another Author" will split into the list
                     #  "Yet","Another" and "Author" and "A.~N.~Other" will
                     #  split into "A","N" and "Other". The idea then is
                     #  that we take the last item as the surname, and we use
                     #  the first characters from the others as the initials.
                     
                     #  To complicate things, we need to distinguish between
                     #  "\~" (which we need to keep; it generates a diacritical
                     #  tilde, or virgulilla, for Spanish words) and '~' which
                     #  is just a space and which we want to drop. What's done
                     #  here is messy - turn "\~" into "\twiddle" and then
                     #  revert - but it works.
                     
                     SlashTwiddle = Author.find("\\~")
                     if (SlashTwiddle >= 0) :
                        Author = Author.replace("\\~","\\twiddle")
                        
                     Author = Author.replace('~',' ').replace('.',' ').strip()
                     
                     if (SlashTwiddle >= 0) :
                        Author = Author.replace("\\twiddle","\\~")
                     
                     #  Ignore any leading 'and', but there ought to be one
                     #  for the last of more than one author, and not in any
                     #  other case.
                     
                     AndExpected = (Index == (Len - 1) and Len > 1)
                     if (Author.startswith("and")) :
                        Author = Author[4:]
                        if (not AndExpected) :
                           Note = "Note: unexpected 'and' before last author"
                           Notes.append(Note)
                     else :
                        if (AndExpected) :
                           Note = "Note: 'and' missing from last of " + \
                                                       "multiple authors"
                           Notes.append(Note)
                            
                     NameList = Author.split()
                     
                     #  Check for some of the more obvious examples of
                     #  the 'on behalf of the rest of the team' type of
                     #  final 'author'.
                     
                     IffyNames = ""
                     IffyCount = 0
                     for Name in NameList :
                        LowerName = Name.lower()
                        if (LowerName == "on" or LowerName == "behalf" or 
                              LowerName == "team" or LowerName == "the" or
                                 LowerName == "of") :
                           if (IffyCount == 0) :
                              IffyNames = Name
                           else : 
                              IffyNames = IffyNames + ', ' + Name
                           IffyCount = IffyCount + 1
                     if (IffyCount > 0) :
                        Notes.append("The following may not be real names: " + \
                                                                      IffyNames)
                                            
                     #  We assume the last is the surname. We then look back
                     #  from that, looking for possible multi-name surnames,
                     #  like "Van der Waals". Each time we find one, we
                     #  prepend it and go back one more. A variation on this 
                     #  is if there is a suffix like "Jr", "Sr", or even "II"
                     #  or "III" or more.
                     
                     NumNames = len(NameList)
                     if (NumNames > 0) :
                     
                        Suffix = ""
                        Surname = NameList[NumNames - 1]
                        if (NumNames > 1) :
                           if (Surname.lower() == "jr") :
                              Suffix = "Jr."
                           elif (Surname.lower() == "sr") :
                              Suffix = "Sr."
                           elif (Surname == "II" or Surname == "III" or
                                    Surname == "IV" or Surname == "V") :
                              Suffix = Surname
                           if (Suffix != "") :
                              NumNames = NumNames - 1
                              Surname = NameList[NumNames - 1]
                        
                        #  Check for unusual examples of upper or lower case
                        #  in the surname. (This picks up cases such as
                        #  "and all my co-workers".)
                        
                        FirstLetter = True
                        PrevChar = ''
                        PrevChars = ""
                        for Char in Surname :
                           if (FirstLetter) : 
                              if (Char.islower()) :
                                 Notes.append("Surname '" + Surname + "'" + \
                                                      " starts in lower case")
                              FirstLetter = False
                           else :
                              if (Char.isupper() and PrevChar != '-' and \
                                    PrevChar != "'" and PrevChars != "Mac" \
                                                       and PrevChars != "Mc") :
                                 Notes.append("Surname '" + Surname + "'" + \
                                            " contains upper case characters")
                                 break
                           PrevChar = Char
                           PrevChars = PrevChars + Char
                                    
                        NumNames = NumNames - 1
                        Multiple = False
                        while (NumNames > 0) :
                           PrevName = NameList[NumNames - 1]
                           if (PrevName.lower() == "van" or \
                                 PrevName.lower() == "de" or \
                                   PrevName.lower() == "den" or \
                                     PrevName.lower() == "von" or \
                                       PrevName.lower() == "le" or \
                                          PrevName.lower() == "da" or \
                                             PrevName.lower() == "der") :
                              Surname = PrevName + ' ' + Surname
                              Multiple = True
                              NumNames = NumNames - 1
                           else :
                              break
                        if (Multiple) :
                           Notes.append(Surname + " assumed to be a surname")
                        
                        #  At this point we have the surname, and NumNames
                        #  should be the number of forenames/initials.
                        
                        NameString = Surname + ','
                        
                        #  This is an attempt to trap the 'Spanish surname'
                        #  case, where Mario Vargas Llosa's surname is actually
                        #  Vargas Llosa. If there is more than one forename,
                        #  and if the last is spelled out, we may have such a
                        #  name. We should at least make a note of it.
                        
                        if (NumNames > 1) :
                           LastForename = NameList[NumNames - 1]
                           Letters = 0
                           for Char in LastForename :
                              if (Char.isupper() or Char.islower()) :
                                 Letters = Letters + 1
                           if (Letters > 1) :
                              Notes.append("Might '" + LastForename + ' ' \
                                             + Surname + "' be a surname?")
                     
                        #  If the surname is a single letter and the forename(s)
                        #  are longer, this might be a case where the names
                        #  have been given with the surname last instead of
                        #  first.
                        
                        if (len(Surname) == 1) :
                           if (NumNames > 0) :
                              if (len(NameList[0]) > 1) :
                                 if (not OrderWarning) :
                                    Notes.append(
                                       "Names should end with the surname")
                                    OrderWarning = True
                                 Notes.append("Might " + NameList[0] + ' ' + \
                                    Surname + " have been given surname first?")
                        
                        #  Now reduce the forenames to initials.
                        
                        InitialCount = 0
                        for Forename in NameList[:NumNames] :
                           Initial = GetInitial(Forename,0,Notes)
                           InitialCount = InitialCount + 1
                           
                           #  This bit is being clever and combining pairs
                           #  of hyphenated initials, catching cases like
                           #  Jean-Luc Picard or even J.-L. Picard (the
                           #  former will have been split into two strings,
                           #  the latter into three).
                           
                           if (Initial == '-') :
                              Initial = GetInitial(Forename,1,Notes)
                              NameString = NameString + '-' + Initial + '.'
                           else :
                              NameString = NameString + '~' + Initial + '.'
                              DashIndex = Forename.find('-')
                              if (DashIndex > 0) :
                                 Initial = \
                                    GetInitial(Forename,DashIndex + 1,Notes)
                                 NameString = NameString + '-' + Initial + '.'
                        if (Suffix != "") :
                           NameString = NameString + ",~" + Suffix
                        AuthorList.append(NameString)
                        if (InitialCount == 0) :
                           if (len(Surname) == 1) :
                              Notes.append("Might " + Surname + \
                                                     " be a misplaced initial?")
                           else :
                              Notes.append(
                                        Surname + " seems to be just a surname")
                  
                  #  If we had any problems, we append the raw author list
                  
                  if (len(Notes) > 0) :
                     Notes.append(RawAuthors)
                     
# ------------------------------------------------------------------------------

#                         G e t   A u t h o r s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for the author list
#   in the paper and returns a list of authors (as generated by the callback
#   routine AuthorScanCallback) with an entry for each author in the form
#   required as the argument to an \aindex directive, eg "Shortridge,~K.".
#   Notes is a list to which this adds a brief description of anything 
#   possibly amiss that it comes across when processing the author list.



def GetAuthors (Paper,Notes,TexFileName = "") :

   AuthorList = []
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      print "Cannot find main .tex file",TexFileName
   else :

      #  Now get a list of the authors from the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call AuthorScanCallback for each command it
      #  finds in the file, and AuthorScanCallback will check the command
      #  and add the list of authors to AuthorList.
      
      Finished = False
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(AuthorScanCallback,\
                                                      AuthorList,Notes)
                                                         
      TexFile.close()

   return AuthorList

# ------------------------------------------------------------------------------

#                         F i x  C h a r a c t e r s
#
#   This routine scans a Line read from a .tex file and checks for some of 
#   the more common foreign accented characters that can cause problems for an
#   English implementation of LaTeX. If it finds any that it recognises, it
#   replaces them with the equivalent LaTeX sequence - for example, it will
#   replace 0xe7 (the Ascii code for c-cedilla) with "\c{c}". If it makes no
#   changes to the string, it will return None. Otherwise it returns the 
#   modified string. The line number passed is used to output a message 
#   describing any changes made. (Pass it as zero to suppress such messages.)
#
#   LaTeX_Chars is a dictionary giving the LaTeX sequences equivalent to the
#   accented unprintable ASCII characters (given as their hex values) recognised
#   by FixCharacters().
#
#   Note: the entry for 0xd5 is unusual: It should really generate "\~{O}"
#   to produce a capital O with a tilde above it. However, it seems that a
#   number of files have this character used for a posessive apostrophe.
#   I am still not entirely sure how this comes about, but this seems to be
#   a more common case than the tilded capital O.

__LaTeX_Chars__ = \
    { 0xc0:"\\`{A}", 0xc1:"\\'{A}", 0xc2:"\\^{A}", 0xc3:"\\~{A}", \
      0xc4:'\\"{A}', 0xc5:"\\.{A}", \
      0xc7:"\\c{C}", \
      0xc8:"\\`{E}", 0xc9:"\\'{E}", 0xca:"\\^{E}", 0xcb:"\\~{E}", \
      0xcc:"\\`{I}", 0xcd:"\\'{I}", 0xce:"\\^{I}", 0xcf:"\\~{I}", \
      0xd1:"\\~{N}", \
      0xd2:"\\`{O}", 0xd3:"\\'{O}", 0xd4:"\\^{O}", 0xd5:"'",      \
      0xd6:'\\"{O}', 0xd8:'\\o{O}', \
      0xd9:"\\`{U}", 0xda:"\\'{U}", 0xdb:"\\^{U}", 0xdc:'\\"{U}', \
      0xdd:"\\'{Y}", 0xdf:"{\\ss}", \
      0xe0:"\\`{a}", 0xe1:"\\'{a}", 0xe2:"\\^{a}", 0xe3:"\\~{a}", \
      0xe4:'\\"{a}', 0xe5:"\\.{a}", \
      0xe7:"\\c{c}", \
      0xe8:"\\`{e}", 0xe9:"\\'{e}", 0xea:"\\^{e}", 0xeb:"\\~{e}", \
      0xec:"\\`{i}", 0xed:"\\'{i}", 0xee:"\\^{i}", 0xef:"\\~{i}", \
      0xf1:"\\~{n}", \
      0xf2:"\\`{o}", 0xf3:"\\'{o}", 0xf4:"\\^{o}", 0xf5:"\\~{o}", \
      0xf6:'\\"{o}', 0xf8:'\\o{o}', \
      0xf9:"\\`{u}", 0xfa:"\\'{u}", 0xfb:"\\^{u}", 0xfc:'\\"{u}', \
      0xfd:"\\'{y}", 0xff:'\\"{y}' }      

def FixCharacters (Line,LineNumber) :

   NewLine = None
   
   #  Quick pass to see if we have a problem
   
   Problem = False
   for Char in Line :
      if (not Char in string.printable) :
         Problem = True
         break
   
   if (Problem) :
      NewLine = ""
      for Char in Line :
         if (Char in string.printable) :
            NewLine = NewLine + Char
         else :
            Num = ord(Char)
            Repl = __LaTeX_Chars__.get(Num)
            if (Repl == None) :
               print "Unexpected unprintable character (" + hex(Num) + \
                                         ") in .tex file at line",LineNumber
               NewLine = NewLine + Char
            else :
               print "Unprintable character (" + hex(Num) + \
                  ") in .tex file at line",LineNumber,"replaced by",Repl
               NewLine = NewLine + Repl
         
   return NewLine 

# ------------------------------------------------------------------------------

#                         C h e c k  C h a r a c t e r s
#
#   This is a version of FixCharacters() that only checks to see there are
#   any potential unprintable-character problems in the line it is passed.
#   It returns True if there were such characters, False otherwise. If there
#   is a known-fix for the problem character, it notes it. The final optional
#   Problems argument allows this to be used in batch mode, where direct output
#   from this routine is suppressed and instead a set of report lines are added
#   to the list of problems passed.
#

def CheckCharacters (Line,LineNumber,Problems = None) :

   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   Problem = False
   for Char in Line :
      if (not Char in string.printable) :
         Problem = True
         Num = ord(Char)
         Repl = __LaTeX_Chars__.get(Num)
         if (Repl == None) :
            Text = "Unexpected unprintable character (" + hex(Num) + \
               ") in .tex file at line " + str(LineNumber)
         else :
            Text = "Unprintable character (" + hex(Num) + \
               ") in .tex file at line " + str(LineNumber) + \
                                       " should be replaced by " + Repl
         if (BatchMode) : Problems.append(Text)
         else : print Text
   
   return Problem 
 
# ------------------------------------------------------------------------------

#                         A u t h o r  C h a r s
#
#   AuthorChars() is passed an author name replete with LaTeX formatting,
#   generally for accented characters. It returns a simplified version of
#   the name, with any of the common accenting syntaxes replaced by, in most
#   cases, just the unaccented character. The exception is the unlaut, where
#   it appends an extra 'e', following the usual convention for writing 
#   German words where the umlaut is too awkward. The author name is also
#   truncated at a comma, so "Surname, I." is truncated to "Surname".
#
#   The idea here is to generate a name that would match that used for the
#   directory name used for a paper by this author, so that this can be
#   checked.
#
#   LaTeX uses a number of special constructs of the form \<char>{<letter>}
#   which modify a single letter to produce an accented character. For example,
#   \c{c} which generates a c-cedilla, or \"{u} which generates a 'u' with an
#   umlaut. LaTeX also accepts the simplified form \<char><letter> in most
#   cases. This code handles \` \' \^ \~ \" \. \c \o \v \H \k \= \b \d \r \u
#   There are probably some other obscure cases out there, but that's a 
#   good start.

def AuthorChars (Author) :

   #  Truncate at a comma - assuming this clips off any trailing initials.
   
   Index = Author.find(',')
   if (Index >= 0) : Author = Author[:Index]
   
   #  If there are no LaTeX directives at all, that's all we have to do.
   
   if (Author.find('\\') >= 0):
   
      #  Work through all the possible values for <char> in \<char>
       
      for Char in "`'^~\".covHk=bdru" :
      
         #  For each character, we try twice, once for the case where the
         #  accented letter is in {braces} and then once where it isn't.
         #  Offset is the number of characters after the '\' where we find
         #  the accented letter itself.
         
         for Try in [1,2] :
            if (Try == 1) :
               Directive = '\\' + Char + '{'
               Offset = 3
            else :
               Directive = '\\' + Char
               Offset = 2
               
            #  We keep going until we've removed each instance of the
            #  directive we're looking for,
            
            while (True) :
               Index = Author.find(Directive)
               if (Index < 0) : break
               
               #  Normally, we just replace the accenting directive with
               #  the single letter. For an umlaut, we append an 'e'
               
               Letter = Author[Index + Offset]
               FullString = Directive + Letter
               if (Try == 1) : FullString = FullString + '}'
               if (Char == '"') : Letter = Letter + 'e'
               Author = Author.replace(FullString,Letter)
               
         #  And we quite once there are no LaTeX directives left.
         
         if (Author.find('\\') < 0): break
         
   return Author
         
# ------------------------------------------------------------------------------

#                         G e t  A r c h i v e  T i m e
#
#   GetArchiveTime() returns the latest modification date (as a time in seconds
#   since the epoch) of any file contained in the named archive file, which
#   can be a .tar, .tar.gz or a .zip file.  If it cannot determine the date
#   it returns None. Optionally, it can also be passed a list to which will
#   be added the names of all the files in the archive.

def GetArchiveTime (Filename,FileList = None) :

   LatestTime = None
   if (Filename.endswith(".tar") or Filename.endswith(".tar.gz") or \
           Filename.endswith(".zip")) : 
      
      #  Remember the current directory and the absolute path of the file
      #  we've been passed (which may have been a relative name)
         
      OriginalDir = os.getcwd()
      AbsFilename = os.path.abspath(Filename)
      AbsFilename = AbsFilename.replace("'","\\'")
      AbsFilename = AbsFilename.replace(" ","\\ ")
      
      #  Create a temporary directory for the files in the archive, move
      #  to it and copy the archive files into it. (This is slower but more
      #  reliable than trying to interpret the output from commands like
      #  "tar -tvf")
      
      TempDir = tempfile.mkdtemp()
      os.chdir(TempDir)
      if (AbsFilename.endswith(".zip")) :
         os.popen("unzip " + AbsFilename)
      else :   
         os.popen("tar -xf " + AbsFilename)
      
      #  Now we'll go through all the files looking at the dates. One
      #  complication - the top level of the archive may be a single
      #  directory which itself holds the files. If so, we dive into that
      #  intermediate directory. (It would probably be better to do a 
      #  recursive search through the whole of the directory.) Also ignore
      #  the __MACOSX files that sometimes end up in OS X archives.
      
      FilesInDir = os.listdir(".")
      FileCount = 0
      IntermediateDir = ""
      LastFile = ""
      for File in FilesInDir :
         if (not File.startswith('.') and File != "__MACOSX") :
            LastFile = File
            FileCount = FileCount + 1
      if (FileCount == 1) :
         IntermediateDir = os.path.abspath(LastFile)
         if (os.path.isdir(IntermediateDir)) :
            os.chdir(IntermediateDir)
            FilesInDir = os.listdir(".") 
            
      #  Now look at the modification dates of all the files. (The test for
      #  exists() is because a file may be a link to a file that does not
      #  exist on this system.) And directories will have the current date,
      #  and we don't expect them anyway.
              
      First = True
      for File in FilesInDir :
         if (os.path.exists(File)) :
            if (not os.path.isdir(File)) :
               FileTime = os.stat(File).st_mtime
               if (First) :
                  LatestTime = FileTime
                  First = False
               else :
                  if (FileTime > LatestTime) : LatestTime = FileTime
               
      #  If the caller passed us a file list, add the file names to it.
      
      if (FileList != None) :
         FileList.extend(FilesInDir)
         
      #  Cleaup up after outselves, and return to the directory we started from.
      
      if (TempDir != "") : os.popen("rm -rf " + TempDir)
      os.chdir(OriginalDir)
   return LatestTime
   
# ------------------------------------------------------------------------------

#                      G e t  A r c h i v e  L i s t
#
#   GetArchiveList() walks through every file in the tree whose root is 
#   the directory passed as Path. It looks for any file that might be an 
#   archive file for the paper whose name is passed as Paper. That is, any
#   .tar, .tar.gz or .zip file whose name contains the paper name in some
#   way. It returns a list of the paths of each candidate file, relative to
#   the current directory.

def GetArchiveList (Path,Paper) :

   #  ArchiveWalkCallback() is a nested callback routine that does most of 
   #  the work. It's nested because that's the easiest way for it to get
   #  access to Paper. It gets called for each directory in Path with DirPath
   #  as the directory path and FileList a list of files in the directory. It
   #  adds any candidate files to the list passed as ArchivePath.
    
   def ArchiveWalkCallback(ArchiveList,DirPath,FileList) :
      for File in FileList :
         if (File.endswith(".tar") or File.endswith(".tar.gz") \
                                               or File.endswith(".zip")) :
            Match = False
            Filelower = File.lower()
            Paperlower = Paper.lower()
            
            #  The basic test is to see if the paper name appears in the file
            #  name - as a case-insensitive test.
            
            if (Filelower.find(Paperlower) >= 0) :
               Match = True
            else :
            
               #  Some people call their files O1.4 instead of O1_4, so we
               #  check for that.
               
               if (Filelower.find(Paperlower.replace('-','.')) >= 0) :
                  Match = True
               else :
               
                  #  And some people miss leading zeros from paper numbers,
                  #  using P71 instead of P071.
                  
                  if (Paperlower.startswith("p00")) :
                     if (Filelower.find(Paperlower.replace('p00','p')) >= 0) :
                        Match = True
                  elif (Paperlower.startswith("p0")) :
                     if (Filelower.find(Paperlower.replace('p0','p')) >= 0) :
                        Match = True
            if (Match) :
               FilePath = os.path.join(DirPath,File)
               ArchiveList.append(FilePath)
   
   #  This is the main body of GetArchiveList(). Walk through the supplied
   #  directory structure, calling ArchiveWalkCallback() for each directory 
   #  it contains.
              
   ArchiveList = []
   os.path.walk(Path,ArchiveWalkCallback,ArchiveList)
   
   return ArchiveList
   
# ------------------------------------------------------------------------------

#                   P a c k a g e  S c a n  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for any packages used. Words are the components of a LaTeX
#   directive parsed by the TexScanner. If this is a "\usepackage" directive,
#   this parses the arguments to that directive and checks to see if any of
#   these are non-standard packages. StandardList is a list of any standard
#   packages found, to which this routine appends. Similarly, NonStandard is
#   a list of any non-standard packages found. In fact, no .tex file should
#   need any \usepackage directives, other than \usepackage{asp2014} as that
#   the standard package itself includes all the standard packages.

__StandardPackages__ = \
   {"array","txfonts","ifthen","lscape","index","graphicx","asmsymb", \
    "wrapfig","chapterbib","url","ncccropmark","watermark"}

def PackageScanCallback(Words,StandardList,NonStandard) :

   NumberWords = len(Words)
   if (NumberWords > 1) :
      if (Words[0] == "\\usepackage") :
         for Word in Words[1:NumberWords] :
            if (Word.startswith('{')) :
               Packages = Word.strip("{}").replace(' ','').split(',')
               Len = len(Packages)
               if (Len > 0) :
                  for Package in Packages :
                     if (Package != "asp2014" and Package != "./asp2014") :
                        Standard = False
                        for StandardPkg in __StandardPackages__ :
                           if (Package == StandardPkg) :
                              Standard = True
                        if (Standard) :
                           StandardList.append(Package)
                        else :
                           NonStandard.append(Package)

# ------------------------------------------------------------------------------

#                        C h e c k   P a c k a g e s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any LaTeX packages
#   used by this .tex file. It lists all the packages found, noting the use
#   of standard packages (which is OK, but unnecessary), and warning about
#   the use of any non-standard packages.
# 
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.
#
#   This routine returns True if everything looks OK, False otherwise.


def CheckPackages (Paper,TexFileName = "",Problems = None) :
   
   ReturnOK = True
   
   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print Problem
      ReturnOK = False
   else :

      #  Now get a list of the packages from the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call PackageScanCallback for each command it
      #  finds in the file, and PackageScanCallback will check the command
      #  and add any packages to one of the two lists.
      
      Finished = False
      StandardList = []
      NonStandard = []
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(PackageScanCallback,\
                                                   StandardList,NonStandard)
                                                         
      TexFile.close()
      
      if (len(StandardList) > 0) :
         if (not BatchMode) :
            print ""
            print "Note:",TexFileName,\
                                 "includes the following standard package(s):"
            for Package in StandardList :
               print "   ",Package
            print "this is OK, but unnecessary."
      if (len(NonStandard) > 0) :
         if (not BatchMode) : print ""
         Problem = TexFileName + \
                         " includes the following non-standard package(s):"
         if (BatchMode) : Problems.append(Problem)
         else : print "**",Problem
         Packages = ""
         for Package in NonStandard :
            Packages = Packages + Package + " "
         if (BatchMode) : Problems.append(Packages)
         else : print Packages
         Problem = "this may be a problem"
         if (BatchMode) : Problems.append(Problem)
         else : print Problem,"**"
         ReturnOK = False

   return ReturnOK

# ------------------------------------------------------------------------------

#                   R u n n i n g  H e a d s  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file for the \markboth directive used to generate the running
#   heads for the paper. Words are the components of a LaTeX directive parsed
#   by the TexScanner. If this is a "\markboth" directive, this parses the 
#   arguments to that directive and checks them for the sort of problems that
#   have occasionally shown up in ADASS papers. Notes should be a list of 
#   strings, initially set empty. Each time the callback encounters a
#   \markboth directive it appends to Notes two strings giving the author
#   list and the paper title. It then adds strings describing any problems
#   it has found. Since any paper should only include one \markboth directive,
#   after the paper has been scanned, Notes should contain exactly two strings. 
#   If Notes is empty, no \markboth has been found, If it contains more than
#   two strings, some problem has been found.

def RunningHeadsCallback(Words,Notes,Unused) :

   NumberWords = len(Words)
   if (NumberWords > 1) :
      if (Words[0] == "\\markboth") :
         if (len(Notes) > 0) :
            Problem = "Paper contains multiple \\markboth directives"
         if (NumberWords != 3) :
            Problem = "\\markboth directive has wrong number of arguments"
            Problems.append(Problem)
         else :
            Authors = Words[1].strip('{}')
            Title = Words[2].strip('{}')
            Note = "Author list for running header is '" + Authors + "'"
            Notes.append(Note)
            Note = "Paper title for running header is '" + Title + "'"
            Notes.append(Note)
            if (Authors == "Author1, Author2, and Author3") :
               Problem = "Author list is unchanged from the template"
               Notes.append(Problem)
            if (Authors.strip() == "") :
               Problem = "Author list is blank"
               Notes.append(Problem)
            if (Title == "Author's Final Checklist") :
               Problem = "Paper title is unchanged from an out-of-date template"
               Notes.append(Problem)
            if (Title == "Short Title") :
               Problem = "Paper title is unchanged from the template"
               Notes.append(Problem)
            if (Title.strip() == "") :
               Problem = "Paper title is blank"
               Notes.append(Problem)
            if (Authors == Title) :
               Problem = "Paper title is the same as the author list"
               Notes.append(Problem)
               
# ------------------------------------------------------------------------------

#                   C h e c k   R u n n i n g  H e a d s
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any \markboth
#   directive that specifies the running heads for the paper (author and
#   title), and checks for any problems with them. (A surprising number of
#   ADASS papers leave the \markboth directive unchanged from the template, or
#   manage to get it wrong in other ways. This routine spots some of the
#   issues that have been seen. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.
# 
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument.
#
#   This routine returns True if everything looks OK, False otherwise.


def CheckRunningHeads (Paper,TexFileName = "",Problems = None) :
   
   ReturnOK = True
   
   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print Problem
      ReturnOK = False
   else :

      #  Now set up to check the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call RunningHeadsCallback for each command it
      #  finds in the file, and RunningHeadsCallback will check the command
      #  and will process any \markboth directive it finds.
      
      Finished = False
      Notes = []
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(RunningHeadsCallback,\
                                                               Notes,None)
                                                         
      TexFile.close()
      
      #  See comments for RunningHeadsCallback() for details of how it handles
      #  Notes. Essentially, if all is well, Notes will have two entries,
      #  which will be the author list and the title list.Anything else
      #  will be an error.
      
      if (not BatchMode) : print ""
      if (len(Notes) == 2) :
         if (not BatchMode) :
            print Notes[0]
            print Notes[1]
      else :
         ReturnOK = False
         if (len(Notes) == 0) :
            Problem = TexFileName + " has no \\markboth directive"
            if (BatchMode) : Problems.append(Problem)
            else : print "**",Problem,"**"
         else :
            Problem = TexFileName + \
             " has problems with the running heads specified using \\markboth:"
            if (BatchMode) : Problems.append(Problem)
            else : print Problem
            for Note in Notes :
               if (BatchMode) : Problems.append(Note)
               else : print "   ",Note
      if (not BatchMode) : print ""

   return ReturnOK

# ------------------------------------------------------------------------------

#                          C i t e  C a l l b a c k
#
#   Used as the callback routine for the TexScanner when it is used to scan
#   the .tex file to see if any references use the old \cite directive. For
#   more details, see RefScanCallback(). This routine adds to CiteRefs the
#   names of any references cited using \cite..

def CiteCallback (Words,CiteRefs,Unused) :

   if (len(Words) > 0) :
      if (Words[0] == "\\cite") :
         Refs = ExtractRefs(Words)
         CiteRefs.append(Refs)
            
# ------------------------------------------------------------------------------

#                          C h e c k   C i t e
#
#   This routine looks in the current directory for a file called 
#   Paper.tex (where Paper will be a string such as "O1-4"), assuming
#   this is the main .tex file for the paper. It looks for any \cite
#   directive and warns about its use.
# 
#   To allow this to be used for preliminary checking, where the main .tex
#   file has been misnamed, the actual .tex file name can be supplied as
#   an optional argument. The final optional Problems argument allows this to
#   be used in batch mode, where direct output from this routine is suppressed
#   and instead a set of report lines are added to the list of problems passed.
#
#   This routine returns True if everything looks OK, False otherwise.


def CheckCite (Paper,TexFileName = "",Problems = None) :
   
   BatchMode = False
   if (Problems != None) : BatchMode = True
   
   ReturnOK = True
   
   if (TexFileName == "") : TexFileName = Paper + ".tex"
   TexFileName = os.path.abspath(TexFileName)
   if (not os.path.exists(TexFileName)) :
      Problem = "Cannot find main .tex file: " + TexFileName
      if (BatchMode) : Problems.append(Problem)
      else : print Problem
      ReturnOK = False
   else :

      #  Now set up to check the .tex file.

      TexFile = open(TexFileName,mode='r')
      TheScanner = TexScanner.TexScanner()
      TheScanner.SetFile(TexFile)
      
      #  GetNextTexCommand() will call CiteCallback for each command it
      #  finds in the file, and CiteCallback will check the command
      #  and will add any reference cited using \cite to CiteRefs..
      
      Finished = False
      CiteRefs = []
      while (not Finished) :
         Finished =  TheScanner.GetNextTexCommand(CiteCallback,CiteRefs,None)
                                                         
      TexFile.close()
      
      if (len(CiteRefs) > 0) :
         Problem = "The .tex file cites the following references using \cite:"
         if (BatchMode) : Problems.append(Problem)
         else : print "**",Problem,"**"
         Refs = ""
         for Ref in CiteRefs :
            Refs = Refs + Ref + " "
         if (BatchMode) : Problems.append(Refs)
         else : print Refs
         Problem = "These should be changed to use \citep or \citet"
         if (BatchMode) : Problems.append(Problem)
         else : print "**",Problem,"**"
         ReturnOK = False

   return ReturnOK
              

