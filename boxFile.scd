(
Box {
	var dur;

	// constructor
	*new { | p |
        ^super.new.init(p)
	}

	// initialize method
	init { | p |
		dur    = 1;
}
}
)

a = Box.new(2)