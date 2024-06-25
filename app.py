{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "17208142-c70f-429d-a923-6a6a16aeccd4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: openai in c:\\users\\user\\new folder\\lib\\site-packages (1.13.3)\n",
      "Requirement already satisfied: flask in c:\\users\\user\\new folder\\lib\\site-packages (2.2.5)\n",
      "Requirement already satisfied: anyio<5,>=3.5.0 in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (4.2.0)\n",
      "Requirement already satisfied: distro<2,>=1.7.0 in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (1.8.0)\n",
      "Requirement already satisfied: httpx<1,>=0.23.0 in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (0.27.0)\n",
      "Requirement already satisfied: pydantic<3,>=1.9.0 in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (2.7.0)\n",
      "Requirement already satisfied: sniffio in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (1.3.0)\n",
      "Requirement already satisfied: tqdm>4 in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (4.65.0)\n",
      "Requirement already satisfied: typing-extensions<5,>=4.7 in c:\\users\\user\\new folder\\lib\\site-packages (from openai) (4.9.0)\n",
      "Requirement already satisfied: Werkzeug>=2.2.2 in c:\\users\\user\\new folder\\lib\\site-packages (from flask) (2.2.3)\n",
      "Requirement already satisfied: Jinja2>=3.0 in c:\\users\\user\\new folder\\lib\\site-packages (from flask) (3.1.3)\n",
      "Requirement already satisfied: itsdangerous>=2.0 in c:\\users\\user\\new folder\\lib\\site-packages (from flask) (2.0.1)\n",
      "Requirement already satisfied: click>=8.0 in c:\\users\\user\\new folder\\lib\\site-packages (from flask) (8.1.7)\n",
      "Requirement already satisfied: idna>=2.8 in c:\\users\\user\\new folder\\lib\\site-packages (from anyio<5,>=3.5.0->openai) (3.4)\n",
      "Requirement already satisfied: colorama in c:\\users\\user\\new folder\\lib\\site-packages (from click>=8.0->flask) (0.4.6)\n",
      "Requirement already satisfied: certifi in c:\\users\\user\\new folder\\lib\\site-packages (from httpx<1,>=0.23.0->openai) (2024.2.2)\n",
      "Requirement already satisfied: httpcore==1.* in c:\\users\\user\\new folder\\lib\\site-packages (from httpx<1,>=0.23.0->openai) (1.0.4)\n",
      "Requirement already satisfied: h11<0.15,>=0.13 in c:\\users\\user\\new folder\\lib\\site-packages (from httpcore==1.*->httpx<1,>=0.23.0->openai) (0.14.0)\n",
      "Requirement already satisfied: MarkupSafe>=2.0 in c:\\users\\user\\new folder\\lib\\site-packages (from Jinja2>=3.0->flask) (2.1.3)\n",
      "Requirement already satisfied: annotated-types>=0.4.0 in c:\\users\\user\\new folder\\lib\\site-packages (from pydantic<3,>=1.9.0->openai) (0.6.0)\n",
      "Requirement already satisfied: pydantic-core==2.18.1 in c:\\users\\user\\new folder\\lib\\site-packages (from pydantic<3,>=1.9.0->openai) (2.18.1)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install openai flask\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "4bfdd9c8-db5f-41d3-bac8-1fe5fa7696cd",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n",
      " * Restarting with watchdog (windowsapi)\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\user\\New folder\\Lib\\site-packages\\IPython\\core\\interactiveshell.py:3561: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, request, jsonify\n",
    "import openai\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "openai.api_key = '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'\n",
    "\n",
    "def get_response(prompt):\n",
    "    response = openai.Completion.create(\n",
    "        engine=\"gpt-3.5-turbo\",  \n",
    "        prompt=prompt,\n",
    "        max_tokens=150,\n",
    "        n=1,\n",
    "        stop=None,\n",
    "        temperature=0.7\n",
    "    )\n",
    "    return response.choices[0].text.strip()\n",
    "\n",
    "@app.route('/chat', methods=['POST'])\n",
    "def chat():\n",
    "    data = request.json\n",
    "    user_input = data.get('message')\n",
    "    \n",
    "    if not user_input:\n",
    "        return jsonify({'error': 'No message provided'}), 400\n",
    "    \n",
    "\n",
    "    prompt = f\"You are TB Advisor, a chatbot specializing in tuberculosis. Answer the following question in a professional and polite manner, including citations from reputable sources: {user_input}\"\n",
    "    \n",
    "\n",
    "    response = get_response(prompt)\n",
    "    \n",
    "    return jsonify({'response': response})\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "cb6d95f1-9d1a-4ab9-8587-f583eacf8935",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
