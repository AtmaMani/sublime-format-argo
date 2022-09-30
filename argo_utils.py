# store in ~/Library/Application\ Support/Sublime\ Text/Packages/User/format_argo.py
import sublime
import sublime_plugin


class FormatArgoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		regions = view.sel()

		# get settings
		settings = sublime.load_settings("Argo Utils.sublime-settings")

		# check if something is selected
		if len(regions) > 1 or not regions[0].empty():
			# iterate over selections
			for region in regions:
				if not region.empty():
					# get original text
					original_text = view.substr(region)

					# modify
					new_text = self._format_argo(original_text, settings)

					# put back
					view.replace(edit, region, new_text)

		
		else:
			# format all text, - no selection
			all_text_region = sublime.Region(0, view.size())
			original_text = view.substr(all_text_region)

			# modify
			new_text = self._format_argo(original_text, settings)

			# put back
			view.replace(edit, region, new_text)

		# set syntax to bash
		if settings.get('set_syntax_to_markdown'):
			view.assign_syntax('Packages/Markdown/Markdown.sublime-syntax')

	
	def _format_argo(self, argo_str, settings):
		"""
		Formats input argo submit command
		"""

		prefix, *lines = argo_str.split(" -p ")

		# sort lines
		if settings.get('alphabetize_parameters'):
			lines = sorted(lines)

		# encapsulate in triple ticks
		if settings.get('encapsulate_in_triple_ticks'):
			ret_str = "```bash\n"
		else:
			ret_str = ""

		suffix="\\"
		ret_str = ret_str + f'{prefix} {suffix}\n'  # argo submit ... line
		for i, line in enumerate(lines):
			a,b = line.split("=")
			if i == len(lines)-1:  # last line
				suffix= ""
			ret_str = ret_str + f'-p {a}={b} {suffix}\n'
			
		if settings.get('encapsulate_in_triple_ticks'):
			ret_str = ret_str + "\n```"

		return ret_str
