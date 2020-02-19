import cli_parser
import input_files_parser
import db_connect
import db_fill
import db_get_data
import output_file_constructor


INPUT_FILES_FORMAT = "json"
DBMS = "mysql"
DB_PARAMS = {"host": "localhost",
             "db_name": "rooms_accounting",
             "user": "user",
             "password": "12345sql"
             }


def main():
    # Get CLI-args
    students_filename, rooms_filename, output_file_format = cli_parser.parse_command_line_args()

    # Parse data from input files
    FileParser = input_files_parser.parsers_for_input_files[INPUT_FILES_FORMAT]
    file_parser = FileParser(students_filename=students_filename,
                             rooms_filename=rooms_filename)
    rooms_objects = file_parser.get_rooms()
    students_objects = file_parser.get_students()

    # Connect to server; create DB, tables (with indexes) if not exists; truncate tables
    DBConnection = db_connect.dbms[DBMS]
    db_connection = DBConnection(**DB_PARAMS)

    db_connection.truncate_tables()
    connection = db_connection.connection

    # Fill out DB with parsed data
    db_filler = db_fill.DBFill(connection, rooms_objects, students_objects)
    db_filler.fill_db()

    # Choose file constructor (json or xml)
    FileConstructor = output_file_constructor.format_handlers[output_file_format]

    # Use functions with SQL-queries and create files.
    get_data = db_get_data.DBGetData(connection)

    db_parser_output_filename = (
        (get_data.rooms_number_of_students, "output_rooms_number_of_student"),
        (get_data.rooms_top5_min_average_age, "output_rooms_top5_min_average_age"),
        (get_data.rooms_top5_max_age_difference, "output_rooms_top5_max_age_difference"),
        (get_data.rooms_with_different_sexes_students, "output_rooms_with_different_sexes_students")
    )

    for db_parser, output_filename in db_parser_output_filename:
        data_format, data_sequence = db_parser()
        file_constructor = FileConstructor(data_sequence, data_format)
        file_constructor.construct_file(output_filename)

    connection.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)
    else:
        print("Done.")
