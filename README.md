# Distributed System Project

This project implements a distributed system using modern Python technologies and best practices.

## Features

- FastAPI-based REST API
- Asynchronous processing
- Kafka for message queuing

## Prerequisites

- Python 3.8+
- Kafka (if running locally)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ovimasbul83/Sentry-Distributed-Systems.git
cd Sentry-Distributed-Systems
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the kafka server (if running locally)
2. Run the application:
```bash
cd app
python main.py
```

## Development

- Code formatting: `black .`

## Project Structure

```
distributed-system/
├── app/
│   ├── api/
│   ├── core/
│   └── kafka_test/
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
