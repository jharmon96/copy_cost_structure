import os
import csv
import settings
import standard_functions
import time
from selenium.webdriver.support.ui import Select

# Used in case of export
output_file = []
output_dict = []


def cs_export_process():
    find_cost_structure_key(settings.cost_structure)
    summary("Export")
    labor_costs("Export")
    ODC_costs("Export")
    indirect_costs("Export")
    indirect_cost_rates("Export")
    print(settings.cost_structure + " successfully exported...")


def cs_import_process():
    add_cost_structure()
    summary("Import")
    find_cost_structure_key(settings.cost_structure)
    labor_costs("Import")
    ODC_costs("Import")
    indirect_costs("Import")
    indirect_cost_rates("Import")


def cs_copy_process():
    cs_export_process()
    print(settings.cost_structure + " successfully exported...")

    add_cost_structure()
    summary("Import")
    print(settings.new_cost_structure + " successfully created...")

    find_cost_structure_key(settings.new_cost_structure)
    labor_costs("Import")
    print("Labor cost elements successfully copied...")

    ODC_costs("Import")
    print("ODCs successfully copied...")

    indirect_costs("Import")
    print("Indirect cost formulas successfully copied...")

    indirect_cost_rates("Import")
    print("Indirect cost rates successfully copied...")


###################################################
# Options list to determine which process to run

options = {"Export": cs_export_process,
           "Import": cs_import_process,
           "Copy": cs_copy_process
           }

###################################################


# kick off process depending on Export, Import, or Copy
def run():
    options[settings.direction]()


def add_cost_structure():
    navigate()
    xpathId = '//*[@id="action-links"]/ul/li/a'
    settings.driver.find_element_by_xpath(xpathId).click()


def find_cost_structure_key(cost_structure_name):
    webPage = settings.URL + r'/action/admin/setup/project/cost_structures/list'
    settings.driver.get(webPage)

    tbody = settings.driver.find_element_by_xpath('//*[@id="body"]/div/div[2]/table/tbody/tr/td/form/table/tbody[1]')
    trs = tbody.find_elements_by_tag_name('tr')

    # Loops through cost structures and looks for the key associated with the name the user provides. Uses this to
    # open the right page.

    for tr in trs:
        tds = tr.find_elements_by_tag_name('td')
        row_cost_structure_key = tr.get_attribute("id")
        if row_cost_structure_key.startswith("k"):
            row_cost_structure_name = tds[2].text

            if row_cost_structure_name == cost_structure_name:
                settings.cost_structure_key = row_cost_structure_key.strip("k_")

    if settings.cost_structure_key == "":
        print("ERROR: Could not find cost structure")
        time.sleep(3)
        settings.driver.quit()
        exit()


def navigate():
    webPage = settings.URL + r"/action/admin/setup/project/cost_structures/list"
    settings.driver.get(webPage)


def summary(direction):
    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.summary_file))

    # If importing, proceed to import function
    if direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            if settings.direction == "Copy":
                cost_structure = settings.new_cost_structure
            else:
                cost_structure = str(row["cost_structure"])
                settings.cost_structure = cost_structure
            cost_structure_key = str(row["cost_structure_key"])
            description = str(row["description"])
            cost_pool_group = str(row["cost_pool_group"])
            active = str(row["active"])

            # Paste name into name field
            xpathId = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[1]/td[2]/input'
            settings.driver.find_element_by_xpath(xpathId).send_keys(cost_structure)

            # Paste description into description field
            xpathId = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[2]/td[2]/textarea'
            settings.driver.find_element_by_xpath(xpathId).send_keys(description)

            # Set Cost Pool Group
            #xpathId = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[3]/td[2]/select'
            #settings.driver.find_element_by_xpath(xpathId).send_keys(cost_pool_group)

            # Save page
            Save()
            time.sleep(1)

    # Standard_functions.fileImport()

    # If exporting, create a dictionary containing the values from Unanet
    elif direction == "Export":

        cost_pool_group = ""
        active = ""

        # Open cost structure Summary page
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                                 "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Find and return cost structure name field
        xpath = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[1]/td[2]/input'
        cost_structure = str(settings.driver.find_element_by_xpath(xpath).get_attribute("value"))

        # Find and return description
        xpath = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[2]/td[2]/textarea'
        description = str(settings.driver.find_element_by_xpath(xpath).get_attribute("value"))

        # Assign values to row in dictionary - to be turned into output csv file
        output_dict_row = {"cost_structure": cost_structure, "cost_structure_key": settings.cost_structure_key,
                           "description": description, "cost_pool_group": cost_pool_group, "active": active}

        # Add row to dictionary
        output_dict.append(output_dict_row)

        # Headers of export csv file
        fnames = ["cost_structure", "cost_structure_key", "description", "cost_pool_group", "active"]

        # Send completed dictionary to be exported to csv file
        standard_functions.file_export(output_dict, fnames, settings.summary_file)


def labor_costs(direction):
    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.labor_cost_file))

    # Determines whether or not information is being imported or exported
    if direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:

            if settings.direction == "Copy":
                cost_structure = settings.new_cost_structure
            else:
                cost_structure = str(row["cost_structure"])

            cost_structure_key = settings.cost_structure_key
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                # Open cost structure labor cost page
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit?costStructureSummaryKey=" \
                          + cost_structure_key + "&tabId=tab.costing.labor"
                settings.driver.get(webpage)

            # Loop through table containing cost elements.
            select = Select(settings.driver.find_element_by_name('notAssigned'))
            for option in select.options:
                if cost_element == option.text:
                    # Select the cost element that matches the row in the import file, then click the move
                    # right button
                    option.click()
                    xpathId = '//*[@title="Move Right"]'
                    settings.driver.find_element_by_xpath(xpathId).click()

            current_key = cost_structure_key
            Save()

    elif direction == "Export":

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                                 "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the Labor Costs tab
        xpathId = '//*[@id="tab.costing.labor_head"]/span'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing cost elements, returning values to local variables.
        select = Select(settings.driver.find_element_by_name('Assigned'))
        for option in select.options:
            cost_element = option.text
            cost_element_key = option.get_attribute('value')

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"cost_structure": settings.cost_structure,
                               "cost_structure_key": settings.cost_structure_key,
                               "cost_element": cost_element, "cost_element_key": cost_element_key}
            # Add row to dictionary
            output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "cost_element", "cost_element_key"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.labor_cost_file)


def ODC_costs(direction):
    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.ODC_cost_file))

    # Process for import
    if direction == "Import":

        ODC_num = 0

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            ODC_num = 1 + ODC_num
            if settings.direction == "Copy":
                cost_structure = settings.new_cost_structure
            else:
                cost_structure = str(row["cost_structure"])

            cost_structure_key = settings.cost_structure_key
            expense_type = str(row["expense_type"])
            expense_type_key = str(row["expense_type_key"])
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit?costStructureSummaryKey=" \
                          + cost_structure_key + "&tabId=tab.costing.odc"
                settings.driver.get(webpage)

            # search expense type DB file for key, find associated name
            expense_types_file = csv.DictReader(open(settings.expense_types_file))
            for row2 in expense_types_file:
                if str(row2["expense_type_key"]) == expense_type_key:
                    expense_type_name = str(row2["expense_type_name"])
                    break

            # Loop through table containing cost elements, find and select the one that matches the import file
            select = Select(settings.driver.find_element_by_name('notAssigned'))
            for option in select.options:
                if expense_type_name == option.text:
                    option.click()

                    # Loop through table containing expense types, find and select the one that matches the import file
                    select2 = Select(settings.driver.find_element_by_name('attributes'))
                    for option2 in select2.options:
                        if cost_element == option2.text:
                            option2.click()

                            # click the move right button
                            xpathId = '//*[@title="Move Right"]'
                            settings.driver.find_element_by_xpath(xpathId).click()

            current_key = cost_structure_key

        # If there were ODCs to import, save the page, otherwise continue
        if ODC_num > 0:
            Save()

    # Process for Export
    elif direction == "Export":

        # Get the latest list of expense types & cost elements, return it to csv files to be referenced later
        standard_functions.get_expense_type_data()
        standard_functions.get_cost_element_data()

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                                 "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the ODC Costs tab
        xpathId = '//*[@id="tab.costing.odc_head"]'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing cost elements, returning values to local variables.
        select = Select(settings.driver.find_element_by_name('Assigned'))
        for option in select.options:

            # keys = a combination of the expense type and cost element - split them out here
            keys = option.get_attribute('value')
            expense_type_key = keys.rsplit(";", 1)[0]
            cost_element_key = keys.rsplit(";", 1)[1]

            # search expense type DB file for key, find associated name
            expense_types_file = csv.DictReader(open(settings.expense_types_file))
            for row in expense_types_file:
                if str(row["expense_type_key"]) == expense_type_key:
                    expense_type = str(row["expense_type"])
                    break

            # search cost elements DB file for key, find associated name
            cost_elements_file = csv.DictReader(open(settings.cost_elements_file))
            for row in cost_elements_file:
                if str(row["cost_element_key"]) == cost_element_key:
                    cost_element = str(row["cost_element"])
                    break

            # Assign values to row in dictionary - to be turned into output csv file
            output_dict_row = {"cost_structure": settings.cost_structure,
                               "cost_structure_key": settings.cost_structure_key,
                               "expense_type": expense_type, "expense_type_key": expense_type_key,
                               "cost_element": cost_element, "cost_element_key": cost_element_key}

            # Add row to dictionary
            output_dict.append(output_dict_row)

    # Headers of export csv file
    fnames = ["cost_structure", "cost_structure_key", "expense_type", "expense_type_key", "cost_element",
              "cost_element_key"]

    # Send completed dictionary to be exported to csv file
    standard_functions.file_export(output_dict, fnames, settings.ODC_cost_file)


def indirect_costs(direction):
    # Holds the cost structure key for URL navigation
    current_key = ""

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.indirect_cost_file))

    # Determines whether or not information is being imported or exported
    if direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            if settings.direction == "Copy":
                cost_structure = settings.new_cost_structure

            else:
                cost_structure = str(row["cost_structure"])

            cost_structure_key = settings.cost_structure_key
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])
            indirect_formula = str(row["indirect_formula"])

            # Go to cost structure URL
            webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit?costStructureSummaryKey=" \
                      + cost_structure_key + "&tabId=tab.costing.pool"
            settings.driver.get(webpage)

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit?costStructureSummaryKey=" \
                          + cost_structure_key + "&tabId=tab.costing.pool"
                settings.driver.get(webpage)

            # Add a new cost element
            xpathId = '//*[@id="addRecordLink"]/a'
            settings.driver.find_element_by_xpath(xpathId).click()

            # Give it a name
            xpathId = '//*[@id="addRow"]/td[2]/select'
            settings.driver.find_element_by_xpath(xpathId).send_keys(cost_element)

            # Add the formula
            xpathId = '//*[@id="formulaTxt"]'
            settings.driver.find_element_by_xpath(xpathId).send_keys(indirect_formula)

            # Add the description
            xpathId = '//*[@id="addRow"]/td[4]/textarea'
            settings.driver.find_element_by_xpath(xpathId).send_keys("")

            Save()

            current_key = cost_structure_key

        pass

    elif direction == "Export":

        # Click on the Indirect Costs tab
        xpathId = '//*[@id="tab.costing.pool_head"]/span'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing cost elements, returning values to local variables.
        tbody = settings.driver.find_element_by_xpath(
            '//*[@id="tab.costing.pool"]/form/table/tbody[1]')
        tbody_rows = tbody.find_elements_by_tag_name('tr')

        # For each row in the table, check if it contains a key (strip out blank rows)
        for tbody_row in tbody_rows:
            cost_element_key = tbody_row.get_attribute("id")
            if cost_element_key.startswith("k"):
                # return the number value after "k_" as the cost element key for the given row
                cost_element_key = cost_element_key.strip("k_")

                # return the 4th attribute of that row, the cost element code.
                cost_element_data = tbody_row.find_elements_by_tag_name('td')
                cost_element = cost_element_data[3].text

                indirect_formula = cost_element_data[4].text

                # Assign values to row in dictionary - to be turned into output csv file
                output_dict_row = {"cost_structure": settings.cost_structure,
                                   "cost_structure_key": settings.cost_structure_key, "cost_element": cost_element,
                                   "cost_element_key": cost_element_key, "indirect_formula": indirect_formula}
                # Add row to dictionary
                output_dict.append(output_dict_row)

        # Headers of export csv file
        fnames = ["cost_structure", "cost_structure_key", "cost_element", "cost_element_key", "indirect_formula"]

        # Send completed dictionary to be exported to csv file
        standard_functions.file_export(output_dict, fnames, settings.indirect_cost_file)


def indirect_cost_rates(direction):
    # Holds the cost structure key for URL navigation
    current_key = ""
    current_fiscal_year_key = ""
    i = 1
    first_row = True

    # Read input file specified in settings
    input_file = csv.DictReader(open(settings.indirect_cost_rates_file))

    # Determines whether or not information is being imported or exported
    if direction == "Import":

        # Assign local variables - the value for each column in a particular row
        for row in input_file:
            if settings.direction == "Copy":
                cost_structure = settings.new_cost_structure
            else:
                cost_structure = str(row["cost_structure"])

            cost_structure_key = settings.cost_structure_key
            cost_element = str(row["cost_element"])
            cost_element_key = str(row["cost_element_key"])
            target_rate = str(row["target_rate"])
            provisional_rate = str(row["provisional_rate"])
            actual_rate = str(row["actual_rate"])
            fiscal_year = str(row["fiscal_year"])
            fiscal_year_key = str(row["fiscal_year_key"])

            # If new cost structure key, navigate to the correct page
            if cost_structure_key != current_key:
                # Open cost structure Summary page
                # Go to cost structure URL
                webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit?costStructureSummaryKey=" \
                          + cost_structure_key + "&tabId=tab.costing.poolRate"
                settings.driver.get(webpage)

            # If new fiscal year key, add a fiscal year
            if fiscal_year_key != current_fiscal_year_key:
                if not first_row:
                    Save()
                # Add a new Indirect Rate
                xpathId = '//*[@id="addRecordLink"]/a'
                settings.driver.find_element_by_xpath(xpathId).click()
                i = 1
                first_row = False

            # search fiscal year DB file for key, find associated name
            fiscal_years_file = csv.DictReader(open(settings.fiscal_years_file))
            for row2 in fiscal_years_file:
                if str(row2["fiscal_year_key"]) == fiscal_year_key:
                    fiscal_year = str(row2["fiscal_year"])
                    break

            # Pick Fiscal Year
            select = Select(settings.driver.find_element_by_name('fiscalYear'))
            for option in select.options:
                if fiscal_year == option.text:
                    option.click()

            # Find cost element row and enter rates
            settings.driver.find_element_by_xpath('//*[@id="addSection"]/tr[' + str(i) + ']/td[3]/input').send_keys(
                target_rate)
            settings.driver.find_element_by_xpath('//*[@id="addSection"]/tr[' + str(i) + ']/td[4]/input').send_keys(
                provisional_rate)
            settings.driver.find_element_by_xpath('//*[@id="addSection"]/tr[' + str(i) + ']/td[5]/input').send_keys(
                actual_rate)

            i = i + 1

            current_key = cost_structure_key
            current_fiscal_year_key = fiscal_year_key

        Save()

    elif direction == "Export":

        fiscal_year = ""

        # Go to cost structure URL
        webpage = settings.URL + "/action/admin/setup/project/cost_structures/edit" \
                                 "?costStructureSummaryKey=" + settings.cost_structure_key
        settings.driver.get(webpage)

        # Click on the Indirect Costs tab
        xpathId = '//*[@id="tab.costing.poolRate_head"]/span'
        settings.driver.find_element_by_xpath(xpathId).click()

        # Loop through table containing rates by fiscal year / cost element
        table = settings.driver.find_element_by_xpath('//*[@id="tab.costing.poolRate"]/form/table')
        tbodys = table.find_elements_by_tag_name('tbody')

        # For each sub table (fiscal year) in the table
        for tbody in tbodys:
            fiscal_year_key = tbody.get_attribute("id")
            if fiscal_year_key.startswith("k"):

                # return the number value after "k_" as the fiscal year key for the given row
                fiscal_year_key = fiscal_year_key.strip("k_")

                trs = tbody.find_elements_by_tag_name('tr')

                # For each row in the fiscal year
                for tr in trs:
                    rates_data = tr.find_elements_by_tag_name('td')

                    # Pull values from row attributes
                    cost_element = rates_data[2].text
                    target_rate = rates_data[3].text
                    provisional_rate = rates_data[4].text
                    actual_rate = rates_data[5].text

                    cost_element_key = "1"

                    # Assign values to row in dictionary - to be turned into output csv file
                    output_dict_row = {"cost_structure": settings.cost_structure,
                                       "cost_structure_key": settings.cost_structure_key, "cost_element": cost_element,
                                       "cost_element_key": cost_element_key, "target_rate": target_rate,
                                       "provisional_rate": provisional_rate, "actual_rate": actual_rate,
                                       "fiscal_year": fiscal_year, "fiscal_year_key": fiscal_year_key}

                    # Add row to dictionary
                    output_dict.append(output_dict_row)

        # Headers of export csv file
        fnames = ["cost_structure", "cost_structure_key", "cost_element", "cost_element_key", "target_rate",
                  "provisional_rate", "actual_rate", "fiscal_year", "fiscal_year_key"]

        # Send completed dictionary to be exported to csv file
        standard_functions.file_export(output_dict, fnames, settings.indirect_cost_rates_file)


def Save():
    # Clicks the save button for most pages
    xpathId = '//*[@id="button_save"]'
    settings.driver.find_element_by_xpath(xpathId).click()

## Code to add eventually ##

# xpath = '//*[@id="tab.costing.summary"]/form/table/tbody/tr[2]/td[2]/textarea'
# description = str(settings.driver.find_element_by_xpath(xpath).get_attribute("value"))

# return_value(DESCRIPTION_PATH, variable_name)
# return_value(createPath(DESCRIPTION_PATH, var, var2, var3), variable_name)
