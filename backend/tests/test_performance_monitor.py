from app.ai.performance_monitor import (
    PerformanceMetric,
    PerformanceMonitor,
)


def test_performance_metric():
    metric = PerformanceMetric(
        name="Retriever",
        elapsed_time=0.1234,
    )

    assert metric.name == "Retriever"
    assert metric.elapsed_time == 0.1234


def test_performance_monitor_initialization():
    monitor = PerformanceMonitor()

    assert monitor._start_times == {}
    assert monitor.metrics == {}


def test_start_timer(monkeypatch):
    monitor = PerformanceMonitor()

    monkeypatch.setattr(
        "app.ai.performance_monitor.time.perf_counter",
        lambda: 10.0,
    )

    monitor.start("Retriever")

    assert "Retriever" in monitor._start_times
    assert monitor._start_times["Retriever"] == 10.0


def test_stop_timer(monkeypatch):
    monitor = PerformanceMonitor()

    times = iter([10.0, 10.25])

    monkeypatch.setattr(
        "app.ai.performance_monitor.time.perf_counter",
        lambda: next(times),
    )

    monitor.start("Retriever")
    elapsed = monitor.stop("Retriever")

    assert elapsed == 0.25
    assert "Retriever" not in monitor._start_times
    assert "Retriever" in monitor.metrics
    assert monitor.metrics["Retriever"].name == "Retriever"
    assert monitor.metrics["Retriever"].elapsed_time == 0.25


def test_stop_without_start_raises_error():
    monitor = PerformanceMonitor()

    try:
        monitor.stop("Retriever")
        assert False
    except ValueError as error:
        assert "No timer started for 'Retriever'." in str(error)


def test_elapsed_for_recorded_metric(monkeypatch):
    monitor = PerformanceMonitor()

    times = iter([5.0, 5.5])

    monkeypatch.setattr(
        "app.ai.performance_monitor.time.perf_counter",
        lambda: next(times),
    )

    monitor.start("LLM")
    monitor.stop("LLM")

    assert monitor.elapsed("LLM") == 0.5


def test_elapsed_for_unknown_metric():
    monitor = PerformanceMonitor()

    assert monitor.elapsed("Unknown") == 0.0


def test_reset():
    monitor = PerformanceMonitor()

    monitor._start_times["Retriever"] = 10.0

    monitor.metrics["LLM"] = PerformanceMetric(
        name="LLM",
        elapsed_time=2.5,
    )

    monitor.reset()

    assert monitor._start_times == {}
    assert monitor.metrics == {}


def test_total_time():
    monitor = PerformanceMonitor()

    monitor.metrics["Retriever"] = PerformanceMetric(
        name="Retriever",
        elapsed_time=0.5,
    )

    monitor.metrics["LLM"] = PerformanceMetric(
        name="LLM",
        elapsed_time=2.0,
    )

    monitor.metrics["Citation"] = PerformanceMetric(
        name="Citation",
        elapsed_time=0.25,
    )

    assert monitor.total_time() == 2.75


def test_total_time_when_empty():
    monitor = PerformanceMonitor()

    assert monitor.total_time() == 0.0


def test_report_when_empty():
    monitor = PerformanceMonitor()

    result = monitor.report()

    assert result == "No performance metrics recorded."


def test_report():
    monitor = PerformanceMonitor()

    monitor.metrics["Retriever"] = PerformanceMetric(
        name="Retriever",
        elapsed_time=0.1234,
    )

    monitor.metrics["LLM"] = PerformanceMetric(
        name="LLM",
        elapsed_time=2.5678,
    )

    result = monitor.report()

    assert "Performance Report" in result
    assert "Retriever" in result
    assert "0.1234 sec" in result
    assert "LLM" in result
    assert "2.5678 sec" in result
    assert "Total Time" in result
    assert "2.6912 sec" in result


def test_display(capsys):
    monitor = PerformanceMonitor()

    monitor.metrics["Retriever"] = PerformanceMetric(
        name="Retriever",
        elapsed_time=0.5,
    )

    monitor.display()

    captured = capsys.readouterr()

    assert "Performance Report" in captured.out
    assert "Retriever" in captured.out
    assert "0.5000 sec" in captured.out


def test_statistics_when_empty(capsys):
    monitor = PerformanceMonitor()

    monitor.statistics()

    captured = capsys.readouterr()

    assert "Performance Statistics" in captured.out
    assert "No metrics recorded." in captured.out


def test_statistics(capsys):
    monitor = PerformanceMonitor()

    monitor.metrics["Retriever"] = PerformanceMetric(
        name="Retriever",
        elapsed_time=0.5,
    )

    monitor.metrics["LLM"] = PerformanceMetric(
        name="LLM",
        elapsed_time=2.0,
    )

    monitor.metrics["Citation"] = PerformanceMetric(
        name="Citation",
        elapsed_time=0.25,
    )

    monitor.statistics()

    captured = capsys.readouterr()

    assert "Performance Statistics" in captured.out
    assert "Stages Recorded : 3" in captured.out
    assert "Fastest Stage" in captured.out
    assert "Citation" in captured.out
    assert "Slowest Stage" in captured.out
    assert "LLM" in captured.out
    assert "Total Time" in captured.out


def test_multiple_timers(monkeypatch):
    monitor = PerformanceMonitor()

    times = iter([
        1.0,   # start Retriever
        1.5,   # stop Retriever
        2.0,   # start LLM
        4.0,   # stop LLM
    ])

    monkeypatch.setattr(
        "app.ai.performance_monitor.time.perf_counter",
        lambda: next(times),
    )

    retriever_time = monitor.start("Retriever")

    assert retriever_time is None

    assert monitor.stop("Retriever") == 0.5

    llm_time = monitor.start("LLM")

    assert llm_time is None

    assert monitor.stop("LLM") == 2.0

    assert monitor.elapsed("Retriever") == 0.5
    assert monitor.elapsed("LLM") == 2.0
    assert monitor.total_time() == 2.5