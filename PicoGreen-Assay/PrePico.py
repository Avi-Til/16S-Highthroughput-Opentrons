import PrePico_fun as fun
import PrePico_var as var

if __name__ == "__main__":

    # Initialize variables
    var.init()
    fun.constcheck()
    # Check for duplicates
    fun.readCSV()
    fun.CSVcheck()
    # Calculate variables
    var.calculate()
    fun.calccheck()
    # Assign decks to well plates
    fun.plate_setup()

    # Create a list for sample distribution
    fun.sources()

    # Summarize variables
    fun.summarize()

    # Display the instructions
    fun.instructions()

    # Write the configuration file
    fun.writeOT()
    