# AI-Agent Framework

This is a minimal framework for experimenting with AI agents, developed at FHGR. It allows for simulation-based agent behavior and data collection through MongoDB.

> ⚠️ **Disclaimer:** This framework is primarily intended for internal or educational use at FHGR. It is not production-ready, lacks extensive documentation and testing, and is not widely adopted. For building robust and production-grade AI agents, consider using mature frameworks such as **LangChain**, **Auto-GPT**, or **CrewAI**.

---

## 🚀 Getting Started

You can run the project using either **Docker** or **Apptainer** (for server environments).

### Option 1: Docker

```bash
docker build -t ai-agent-framework .
docker run -p 5000:5000 ai-agent-framework
```

### Option 2: Apptainer (on server)

```bash
./apptainer-build.sh
./apptainer-run.sh
```

---

## 🧠 Starting a Simulation

Once the system is running, you can start simulations via your browser or an HTTP client:

- Start a default simulation loop:
  ```
  http://localhost:5000/group/start/endless
  ```

- Start a simulation with a custom configuration:
  1. Create your own `.json` config file in the appropriate directory.
  2. Start with:
     ```
     http://localhost:5000/group/start/<yourConfigFileName>
     ```

---

## 📦 MongoDB: Exporting & Importing Data

### Step 1: Install `mongodump`

```bash
wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2404-x86_64-100.12.0.tgz
tar -zxvf mongodb-database-tools-*.tgz
```

### Step 2: Dump Data from Server

```bash
./bin/mongodump --uri="mongodb://localhost:27017" --out=/tmp/mongo_backup
```

### Step 3: Transfer Data to Local Machine

```bash
scp -r username@server.fhgr.ch:/tmp/mongo_backup ./
```

### Step 4: Restore to Local MongoDB

Download and install the database tools for your OS:  
🔗 https://www.mongodb.com/docs/database-tools/installation/installation-windows/

Then run:

```bash
mongorestore --uri="mongodb://root:example@localhost:27017/?authSource=admin" ./mongo_backup
```

---

## 🧑‍💻 Support

If you're from FHGR and have questions or run into problems, feel free to contact me directly. Please note that this project is not under active development, and support may be limited.

---

## 📄 License

This project is provided "as is" for educational and experimental purposes.
