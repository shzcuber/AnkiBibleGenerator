# Bible data structure - books, chapters, and verse counts
# This is a simplified structure for the most common books

BIBLE_BOOKS = {
    # Old Testament
    "Genesis": {
        "chapters": 50,
        "verses_per_chapter": {
            1: 31,
            2: 25,
            3: 24,
            4: 26,
            5: 32,
            6: 22,
            7: 24,
            8: 22,
            9: 29,
            10: 32,
            11: 32,
            12: 20,
            13: 18,
            14: 24,
            15: 21,
            16: 16,
            17: 27,
            18: 33,
            19: 38,
            20: 18,
            21: 34,
            22: 24,
            23: 20,
            24: 67,
            25: 34,
            26: 35,
            27: 46,
            28: 22,
            29: 35,
            30: 43,
            31: 55,
            32: 32,
            33: 20,
            34: 31,
            35: 29,
            36: 43,
            37: 36,
            38: 30,
            39: 23,
            40: 23,
            41: 57,
            42: 38,
            43: 34,
            44: 34,
            45: 28,
            46: 34,
            47: 31,
            48: 22,
            49: 33,
            50: 26,
        },
    },
    "Exodus": {
        "chapters": 40,
        "verses_per_chapter": dict(
            zip(
                range(1, 41),
                [
                    22,
                    25,
                    22,
                    31,
                    23,
                    30,
                    25,
                    32,
                    35,
                    29,
                    10,
                    51,
                    22,
                    21,
                    27,
                    36,
                    16,
                    27,
                    25,
                    26,
                    36,
                    31,
                    33,
                    18,
                    40,
                    37,
                    21,
                    43,
                    46,
                    38,
                    18,
                    35,
                    23,
                    35,
                    35,
                    38,
                    29,
                    31,
                    43,
                    38,
                ],
            )
        ),
    },
    # New Testament
    "Matthew": {
        "chapters": 28,
        "verses_per_chapter": dict(
            zip(
                range(1, 29),
                [
                    25,
                    23,
                    17,
                    25,
                    48,
                    34,
                    29,
                    34,
                    38,
                    42,
                    30,
                    50,
                    58,
                    36,
                    39,
                    28,
                    27,
                    35,
                    30,
                    34,
                    46,
                    46,
                    39,
                    51,
                    46,
                    75,
                    66,
                    20,
                ],
            )
        ),
    },
    "Mark": {
        "chapters": 16,
        "verses_per_chapter": dict(
            zip(
                range(1, 17),
                [45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72, 47, 20],
            )
        ),
    },
    "Luke": {
        "chapters": 24,
        "verses_per_chapter": dict(
            zip(
                range(1, 25),
                [
                    80,
                    52,
                    38,
                    44,
                    39,
                    49,
                    50,
                    56,
                    62,
                    42,
                    54,
                    59,
                    35,
                    35,
                    32,
                    31,
                    37,
                    43,
                    48,
                    47,
                    38,
                    71,
                    56,
                    53,
                ],
            )
        ),
    },
    "John": {
        "chapters": 21,
        "verses_per_chapter": dict(
            zip(
                range(1, 22),
                [
                    51,
                    25,
                    36,
                    54,
                    47,
                    71,
                    53,
                    59,
                    41,
                    42,
                    57,
                    50,
                    38,
                    31,
                    27,
                    33,
                    26,
                    40,
                    42,
                    31,
                    25,
                ],
            )
        ),
    },
    "Acts": {
        "chapters": 28,
        "verses_per_chapter": dict(
            zip(
                range(1, 29),
                [
                    26,
                    47,
                    26,
                    37,
                    42,
                    15,
                    60,
                    40,
                    43,
                    48,
                    30,
                    25,
                    52,
                    28,
                    41,
                    40,
                    34,
                    28,
                    41,
                    38,
                    40,
                    30,
                    35,
                    27,
                    27,
                    32,
                    44,
                    31,
                ],
            )
        ),
    },
    "Romans": {
        "chapters": 16,
        "verses_per_chapter": dict(
            zip(
                range(1, 17),
                [32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 23, 33, 27],
            )
        ),
    },
    "1 Corinthians": {
        "chapters": 16,
        "verses_per_chapter": dict(
            zip(
                range(1, 17),
                [31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40, 58, 24],
            )
        ),
    },
    "2 Corinthians": {
        "chapters": 13,
        "verses_per_chapter": dict(
            zip(range(1, 14), [24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14])
        ),
    },
    "Galatians": {
        "chapters": 6,
        "verses_per_chapter": dict(zip(range(1, 7), [24, 21, 29, 31, 26, 18])),
    },
    "Ephesians": {
        "chapters": 6,
        "verses_per_chapter": dict(zip(range(1, 7), [23, 22, 21, 32, 33, 24])),
    },
    "Philippians": {
        "chapters": 4,
        "verses_per_chapter": dict(zip(range(1, 5), [30, 30, 21, 23])),
    },
    "Colossians": {
        "chapters": 4,
        "verses_per_chapter": dict(zip(range(1, 5), [29, 23, 25, 18])),
    },
    "1 Thessalonians": {
        "chapters": 5,
        "verses_per_chapter": dict(zip(range(1, 6), [10, 20, 13, 18, 28])),
    },
    "2 Thessalonians": {
        "chapters": 3,
        "verses_per_chapter": dict(zip(range(1, 4), [12, 17, 18])),
    },
    "1 Timothy": {
        "chapters": 6,
        "verses_per_chapter": dict(zip(range(1, 7), [20, 15, 16, 16, 25, 21])),
    },
    "2 Timothy": {
        "chapters": 4,
        "verses_per_chapter": dict(zip(range(1, 5), [18, 26, 17, 22])),
    },
    "Titus": {
        "chapters": 3,
        "verses_per_chapter": dict(zip(range(1, 4), [16, 15, 15])),
    },
    "Philemon": {"chapters": 1, "verses_per_chapter": {1: 25}},
    "Hebrews": {
        "chapters": 13,
        "verses_per_chapter": dict(
            zip(range(1, 14), [14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25])
        ),
    },
    "James": {
        "chapters": 5,
        "verses_per_chapter": dict(zip(range(1, 6), [27, 26, 18, 17, 20])),
    },
    "1 Peter": {
        "chapters": 5,
        "verses_per_chapter": dict(zip(range(1, 6), [25, 25, 22, 19, 14])),
    },
    "2 Peter": {
        "chapters": 3,
        "verses_per_chapter": dict(zip(range(1, 4), [21, 22, 18])),
    },
    "1 John": {
        "chapters": 5,
        "verses_per_chapter": dict(zip(range(1, 6), [10, 29, 24, 21, 21])),
    },
    "2 John": {"chapters": 1, "verses_per_chapter": {1: 13}},
    "3 John": {"chapters": 1, "verses_per_chapter": {1: 14}},
    "Jude": {"chapters": 1, "verses_per_chapter": {1: 25}},
    "Revelation": {
        "chapters": 22,
        "verses_per_chapter": dict(
            zip(
                range(1, 23),
                [
                    20,
                    29,
                    22,
                    11,
                    14,
                    17,
                    17,
                    13,
                    21,
                    11,
                    19,
                    17,
                    18,
                    20,
                    8,
                    21,
                    18,
                    24,
                    21,
                    15,
                    27,
                    21,
                ],
            )
        ),
    },
}


def get_book_names():
    """Return a list of all Bible book names."""
    return list(BIBLE_BOOKS.keys())


def get_chapter_count(book_name):
    """Return the number of chapters in a book."""
    if book_name in BIBLE_BOOKS:
        return BIBLE_BOOKS[book_name]["chapters"]
    return 0


def get_verse_count(book_name, chapter):
    """Return the number of verses in a specific chapter."""
    if (
        book_name in BIBLE_BOOKS
        and chapter in BIBLE_BOOKS[book_name]["verses_per_chapter"]
    ):
        return BIBLE_BOOKS[book_name]["verses_per_chapter"][chapter]
    return 0


def format_reference(book, chapter, start_verse, end_verse=None):
    """Format a Bible reference string."""
    if end_verse and end_verse != start_verse:
        return f"{book} {chapter}:{start_verse}-{end_verse}"
    else:
        return f"{book} {chapter}:{start_verse}"
