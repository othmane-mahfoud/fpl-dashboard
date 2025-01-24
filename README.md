# **FPL Dashboard**

## **Overview**

The **Fantasy Premier League (FPL) Dashboard** is a web-based analytics application that provides insightful visualizations for Fantasy Premier League players and teams. It allows users to analyze player performances, compare statistics, and evaluate fixture difficulty.

The app is built using **Dash**, with a backend implemented in **Python**, and dependencies managed using **Poetry**. The project is containerized using **Docker** for consistent deployment.

---

## **Features**

- **Player Performance by Gameweek**: Compare the weekly performances of two players.
- **Player Cost vs. Performance**: Analyze player cost-effectiveness with filtering options (position, team, and budget).
- **ICT Index Breakdown**: Compare influence, creativity, and threat (ICT) values for two players via a radar chart.
- **Fixture Difficulty Ratings**: Visualize and compare the difficulty of fixtures for teams by gameweeks using a heatmap.

---                  

## Getting Started

### Prerequisites

- Python ≥ 3.13
- Poetry ≥ 1.6
- Docker ≥ 20.10.0

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/othmane-mahfoud/fpl-dashboard.git
cd fpl-dashboard
```

2. **Install Dependencies** Use Poetry to install dependencies:
```bash
poetry install
```

3. **Run the Application**
```bash
poetry run python app.py
```

4. **Access the Dashboard** Open your browser and navigate to: [http://127.0.0.1:8050](http://127.0.0.1:8050)

### Using Docker

1. **Build the Docker Image**
```bash
docker build -t fpl-dashboard .
```

2. **Run the Docker Container**
```bash
docker run -p 8050:8050 fpl-dashboard
```

3. **Access the Dashboard** Open your browser and navigate to: [http://0.0.0.0:8050/](http://0.0.0.0:8050/)

## Testing

Unit tests are implemented using **PyTest**.

1. **Run tests**
```bash
poetry run pytest
```

2. **Testing with Docker**
```bash
docker run fpl-dashboard poetry run pytest
```

## Documentation

Project documentation is generated using **Sphinx** and can be found in the `docs/` directory.

1. **Build Documentation**
```bash
poetry run sphinx-build docs/ docs/_build
```

2. **View Documentation** Open the generated HTML in your browser: `docs/_build/index.html`

## Results

Below are some screenshots from the running app.

### Player Performance Comparison by Gameweek
![](assets/screenshots/player_performance_by_gw.png)

### Player Cost vs. Performance
![](assets/screenshots/cost_performance.png)

### ICT Index Breakdown
![](assets/screenshots/ict_index.png)

### Fixtures Difficulty Rating
![](assets/screenshots/fdr.png)

## Author

Othmane Mahfoud <br>
Master in Data Science at University of Luxembourg <br>
Feel free to reach out: `mahfoud.othmane97@gmail.com`
