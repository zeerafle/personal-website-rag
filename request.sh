curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"question": "Who is sam?"}' \
    http://127.0.0.1:8000/ask

# response
# {
#   "answer": [
#     {
#       "type": "text",
#       "text": "Sam is an AI engineering enthusiast who enjoys using machine learning and AI to build things. He has a strong foundation in both the theoretical and practical aspects of these subjects and desires to build impactful solutions and encourage industry innovation. He is currently pursuing a master's degree in AI. In his free time, he enjoys watching and analyzing movies, reading science books, and listening to music. He also holds a Tensorflow Developer Certificate and a Microsoft AI Engineer certificate.",
#       "extras": {
#         "signature": "Ct0BAXLI2nzDsrcVrmUnxZ4+fmohBWW2+Jp7IHlmes2u5mvxQ2ODjG47OBi0u5Hz5IdnPshLt2BVqgaCzknI6FLQYbkDucbKBKUzjVKJn4khbnCzHFgixVViisyEu1gGTC5K0aVfcbmj9MfdRN7LSc+0uYCNFoZ9mXliKoRAa+nhXBYEES5OGZo62Yk3wjfCtfS50C4XnoIq/jkJOApdTIcMJBvZ+fBdSiJh7XVfOLRy+sWuSoMZ4loIRsTOusZDNAzrM4JFwG7ysswGnnwRbuguyU7H1DEbCtbcj8lm/KQ="
#       }
#     }
#   ],
#   "sources": [
#     [
#       {
#         "id": "404_107",
#         "metadata": {
#           "category": "general",
#           "document_type": "general",
#           "file_name": "404",
#           "file_path": "./github_data/_pages/404.md"
#         },
#         "page_content": "title: \"Page Not Found\" excerpt: \"Page not found. Your pixels are in another canvas.\" sitemap: false permalink: /404.html\n\nSorry, but the page you were trying to view does not exist.",
#         "type": "Document"
#       },
#       {
#         "id": "about_111",
#         "metadata": {
#           "category": "general",
#           "document_type": "general",
#           "file_name": "about",
#           "file_path": "./github_data/_pages/about.md"
#         },
#         "page_content": "permalink: /about/ title: \"About\"\n\nI am an AI engineering enthusiast. I enjoy using machine learning and/or AI to build something. I have good foundation in both theoritical and practical parts regarding these subjects. Building an impactful stuff as well as encouraging industry innovation has always been my desire. Currently I'm continuing my study on AI for my master's degree.\n\nI love watching movies and analyzing every aspect of it. Also, I sometimes read science books. And I listen to music very often.\n\nHere I proudly present my Tensorflow Developer Certificate badge.\n\n\n\nAnd my Microsoft AI Engineer certificate here\n\nAnd here is some of my badges I got throughout my learning journey.",
#         "type": "Document"
#       },
#       {
#         "id": "09-student-supervisor-examiner_1",
#         "metadata": {
#           "category": "general",
#           "document_type": "general",
#           "file_name": "09-student-supervisor-examiner",
#           "file_path": "./github_data/_college-notes/season-6/metpen/09-student-supervisor-examiner.md"
#         },
#         "page_content": "title: Student, The Supervisor, and The Examiner\n\nActors Involved, their Roles and Relationship\n\n\n\nStudent\n\nDiscuss with supervisor what kind of guidance\n\nPlan and discuss with supervisor the topic of the project and the timetable\n\nMaintain progress\n\nKeep systematic records of work completed\n\nMake sure submit written material\n\nDecide when it is ready for submission\n\nWrite up submit report within time limit\n\nAddress and respond to criticism, guidance, and suggenstions\n\nBe informed about respect any regulations and considerations, legal as well as ethcial, that are relevant for the project\n\nDrive the project forward\n\nInform supervisor of any problems or difficulties\n\nTake pride in and responsibility, priorities and organize work in suc a way that it represents best efforts.",
#         "type": "Document"
#       }
#     ]
#   ]
# }
