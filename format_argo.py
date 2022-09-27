import sublime
import sublime_plugin


class FormatArgoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		regions = view.sel()

		# check if something is selected
		if len(regions) > 1 or not regions[0].empty():
			# iterate over selections
			for region in regions:
				if not region.empty():
					# get original text
					original_text = view.substr(region)

					# modify
					new_text = self._format_argo(original_text)

					# put back
					view.replace(edit, region, new_text)

		
		else:
			# format all text, - no selection
			all_text_region = sublime.Region(0, view.size())
			original_text = view.substr(all_text_region)

			# modify
			new_text = self._format_argo(original_text)

			# put back
			view.replace(edit, region, new_text)

	
	def _format_argo(self, argo_str):
		"""
		Formats input argo submit command
		"""

		prefix, *lines = argo_str.split(" -p ")

		# sort lines
		lines = sorted(lines)

		ret_str = ""

		suffix="\\"
		ret_str = f'{prefix} {suffix}\n'  # argo submit ... line
		for i, line in enumerate(lines):
			a,b = line.split("=")
			if i == len(lines)-1:  # last line
				suffix= ""
			ret_str = ret_str + f'-p {a}={b} {suffix}\n'
			
		return ret_str
