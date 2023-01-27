if test -t 1; then
	colors=$(tput colors)
	if test $colors -eq 256; then
		echo "Colors Good."
	fi
fi

