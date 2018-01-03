'''
    This service provides a single method to find the most
    closely related song from a given list of songs

    @author : swayam
'''
class BestMatchService:

    '''
        This method is basic implementation of Lavenshtine-Distance
        or simple the Edit-Distance between two strings.
        We return the most closest song as requested by the user.

        reference : https://en.wikipedia.org/wiki/Levenshtein_distance
    '''
    @staticmethod
    def get_best_match(search_list, song):
        if len(search_list) == 0:
            raise Exception("no song found!")

        song_length = len(song)
        best_match_value = song_length
        best_match_index = 0
        for index in range(len(search_list)) :
            search_result = search_list[index]
            search_result_length = len(search_result)
            lavenshtine_matrix = [[0 for x in range(song_length+1)] for x in range(search_result_length+1)]

            for i in range(search_result_length + 1):
                for j in range(song_length + 1):
                    if i == 0:
                        lavenshtine_matrix[i][j] = j
                    elif j == 0:
                        lavenshtine_matrix[i][j] = i
                    elif search_result[i - 1] == song[j - 1]:
                        lavenshtine_matrix[i][j] = lavenshtine_matrix[i - 1][j - 1]
                    else:
                        lavenshtine_matrix[i][j] = 1 + min(lavenshtine_matrix[i][j - 1],        # Insert
                                                           lavenshtine_matrix[i - 1][j],        # Remove
                                                           lavenshtine_matrix[i - 1][j - 1])    # Replace

            if best_match_value > lavenshtine_matrix[search_result_length][song_length]:
                best_match_value = lavenshtine_matrix[search_result_length][song_length]
                best_match_index = index
        return best_match_index