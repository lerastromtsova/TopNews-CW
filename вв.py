        all_words, _ = s.all_words(s.name)
        all_wo_countries, num_all_wo_countries = s.all_wo_countries(all_words)
        all_wo_countries_small, num_all_wo_countries_small = s.all_wo_countries_and_small(all_words)
        fio, num_fio = s.fio(all_words)
        big, num_big = s.big(all_words)
        small, num_small = s.small(all_words)
        countries, num_countries = s.countries(all_words)
        numbers, num_numbers = s.numbers(all_words)
        ids, num_ids = s.ids(all_words)

        unique_words, num_unique_words = s.all_words(s.new_name)
        unique_wo_countries, num_unique_wo_countries = s.all_wo_countries(unique_words)
        unique_wo_countries_small, num_unique_wo_countries_small = s.all_wo_countries_and_small(unique_words)
        unique_fio, unique_num_fio = s.fio(unique_words)
        unique_big, unique_num_big = s.big(unique_words)
        unique_small, unique_num_small = s.small(unique_words)
        unique_countries, unique_num_countries = s.countries(unique_words)
        unique_numbers, unique_num_numbers = s.numbers(unique_words)
        unique_ids, unique_num_ids = s.ids(unique_words)
        frequent_unique = unique_words.intersection(s.most_frequent())