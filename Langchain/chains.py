from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# # prompt template
# prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# # create a chat model
# model = ChatOllama(model="qwen2.5:3b")

# # chain the prompt, model, and output parser
# chain = prompt | model | StrOutputParser()

# # run the chain
# res = chain.invoke({"topic":"bears"})

# print(res)

prompt = ChatPromptTemplate.from_template("tell me history of {country}")

# create a chat model
model = ChatOllama(model="llama3.2")

#chain the prompt, model and output parser
chain = prompt | model | StrOutputParser()

# run the chain
res = chain.invoke({"country":"India"})

print(res)


# What a vast and fascinating topic! The history of India spans thousands of years, with a rich and diverse cultural heritage that has been shaped by various empires, dynasties, and civilizations. Here's a brief overview:

# **Ancient India (3300 BCE - 500 CE)**

# * The Indus Valley Civilization (3300 BCE - 1300 BCE): One of the earliest civilizations in the world, known for its sophisticated urban planning, architecture, and water management systems.
# * The Vedic Period (1500 BCE - 500 BCE): The Vedas, ancient Hindu scriptures, were composed during this period, which saw the rise of the Vedic people and the development of Hinduism.
# * The Mauryan Empire (322 BCE - 185 BCE): Founded by Chandragupta Maurya, this empire is considered one of the greatest empires in Indian history, known for its administrative reforms, infrastructure development, and patronage of the arts.
# * The Gupta Empire (320 CE - 550 CE): This golden age of India saw a resurgence of art, literature, and science, with significant contributions from scholars like Aryabhata and Varahamihira.

# **Medieval India (500 CE - 1500 CE)**

# * The Gupta-Vakataka Period (500 CE - 750 CE): This period saw the rise of regional kingdoms and the decline of the Gupta Empire.
# * The Delhi Sultanate (1206 CE - 1526 CE): Founded by Qutb-ud-din Aibak, this Muslim kingdom saw the introduction of Islam to India and the construction of many iconic mosques and monuments.
# * The Vijayanagara Empire (1336 CE - 1646 CE): A Hindu kingdom that rose to power in southern India, known for its military prowess and cultural achievements.

# **Mughal India (1526 CE - 1756 CE)**

# * The Mughal Empire (1526 CE - 1756 CE): Founded by Babur, this empire saw the rise of the Mughal dynasty, known for its architectural achievements, administrative reforms, and patronage of the arts.
# * The reign of Akbar the Great (1556 CE - 1605 CE): Akbar's tolerant and inclusive policies helped to promote cultural exchange between Hindus and Muslims.
# * The reign of Shah Jahan (1628 CE - 1658 CE): Shah Jahan's construction of the Taj Mahal and other iconic monuments is one of the most famous examples of Mughal architecture.

# **British India (1756 CE - 1947 CE)**

# * The British East India Company (1612 CE - 1858 CE): Founded by James Lancaster, this British company established trade relations with India and eventually expanded its control over the subcontinent.
# * The British Raj (1858 CE - 1947 CE): The British government took over control of India from the East India Company, leading to the imposition of British rule and the erosion of Indian autonomy.
# * The Indian Rebellion of 1857: Also known as the Sepoy Mutiny, this rebellion was a major uprising against British rule, which ultimately led to the establishment of the British Raj.

# **Modern India (1947 CE - present)**

# * The partition of India (1947 CE): The British government divided India into two separate countries: India and Pakistan, leading to one of the largest mass migrations in history.
# * The Indian Independence Movement (1919 CE - 1947 CE): Led by figures like Mahatma Gandhi, Jawaharlal Nehru, and Subhas Chandra Bose, this movement fought for Indian independence from British rule.
# * The Constitution of India (1950 CE): The Constitution of India, which came into effect on January 26, 1950, enshrined the fundamental rights and duties of Indian citizens and established India as a federal republic.
# * The modern era (1947 CE - present): India has experienced significant economic growth, technological advancements, and cultural changes, while also facing challenges like poverty, inequality, and environmental degradation.

# This brief history barely scratches the surface of India's rich and complex past. There is much more to explore and discover about this fascinating country!