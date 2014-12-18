# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re


class TrimmerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view

        matched_regions = view.find_all("[\t ]+$")
        matched_regions.reverse()

        for r in matched_regions:
            view.erase(edit, r)

        sublime.status_message("Trimmer: trailing whitespace removed.")


class DeleteEmptyLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile("^[ \t]*$\r?\n", re.MULTILINE)

        for region in self.selections(view):
            str_buffer = view.substr(region)
            trimmed = reobj.sub("", str_buffer)
            if str_buffer == trimmed:
                sublime.status_message("Trimmer: no empty lines to delete.")
            else:
                view.replace(edit, region, trimmed)
                sublime.status_message("Trimmer: empty lines deleted.")

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions


class RemoveBlankSpaces(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile(r"[ \t\r\n\v\f]")

        for region in self.selections(view):
            trimmed = reobj.sub("", view.substr(region))
            view.replace(edit, region, trimmed)

        sublime.status_message("Trimmer: blanks spaces removed.")

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions


class TrimLeadingWhitespaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile("^[ \t]+", re.MULTILINE)

        for region in self.selections(view):
            trimmed = reobj.sub("", view.substr(region))
            view.replace(edit, region, trimmed)

        sublime.status_message("Trimmer: leading whitespace removed.")

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions


class TrimLeadingTrailingWhitespace(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile("^[ \t]+|[\t ]+$", re.MULTILINE)

        for region in self.selections(view):
            trimmed = reobj.sub("", view.substr(region))
            view.replace(edit, region, trimmed)

        sublime.status_message(
            "Trimmer: leading and trailing whitespace removed.")

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions


class CollapseLines(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile(r"(?:\s{0,})(\r?\n)(?:\s{0,})(?:\r?\n+)")

        for region in self.selections(view):
            str_buffer = view.substr(region)
            trimmed = reobj.sub(r"\1\1", str_buffer)
            if str_buffer == trimmed:
                sublime.status_message("Trimmer: no lines to collapse.")
            else:
                view.replace(edit, region, trimmed)
                sublime.status_message("Trimmer: lines collapsed.")

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions


class CollapseSpaces(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile("([ ]{1})[ ]{1,}")

        for region in self.selections(view):
            str_buffer = view.substr(region)
            trimmed = reobj.sub(r"\1", str_buffer)
            if str_buffer == trimmed:
                sublime.status_message("Trimmer: no spaces to collapse.")
            else:
                view.replace(edit, region, trimmed)
                sublime.status_message("Trimmer: spaces collapsed.")

    def selections(self, view, default_to_all=True):
        regions = [r for r in view.sel() if not r.empty()]
        if not regions and default_to_all:
            regions = [sublime.Region(0, view.size())]
        return regions


class TrimEdges(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        reobj = re.compile(r"(\A\s+|\s+\Z)")

        if view.size() > 0:
            region = sublime.Region(0, view.size())
            trimmed = reobj.sub("", view.substr(region))
            view.replace(edit, region, trimmed)

        sublime.status_message("Trimmer: file edges trimmed.")


class ReplaceSmartCharactersCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        has_matches = False

        """ credit Daryl Tucker
        https://github.com/daryltucker/MagiclessQuotes"""
        replacements = [
            [u'[’‘]{1}', u'\''],
            [u'[“”]{1}', u'"'],
            [u'[…]{1}', u'...'],
            [u'[—]{1}', u'---'],
            [u'[–]{1}', u'--'],
            [u'[•]{1}', u'*']
        ]

        for replacement in replacements:
            x = view.find_all(replacement[0])
            for position in x:
                view.replace(edit, position, replacement[1])
                has_matches = True

        if has_matches:
            sublime.status_message("Trimmer: smart characters replaced.")
        else:
            sublime.status_message("Trimmer: no smart characters to replace.")
