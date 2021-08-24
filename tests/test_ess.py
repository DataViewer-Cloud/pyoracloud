#!/usr/bin/env python

"""Tests for `pyoracloud` package."""


def test_schedule_job_accept_two_args() -> None:
    """SchedulerJob should accept two arguments"""
    from pyoracloud import ess

    package = "package"
    definition = "definition"
    sch_job = ess.SchedulerJob(package, definition)
    assert (
        sch_job.package == package
        and sch_job.definition == definition
        and len(sch_job.parameters) == 0
    )


def test_schedule_job_add_parameter() -> None:
    """SchedulerJob should add parameter to the List"""
    from pyoracloud import ess

    inputParam = ["P1", "P2"]

    sch_job = ess.SchedulerJob("package", "definition")
    for p in inputParam:
        sch_job.add_parameter(p)
    assert all(
        [actual == expected for actual, expected in zip(sch_job.parameters, inputParam)]
    )


def test_schedule_job_null_parameter() -> None:
    """ScheduleJob should return #NULL as parameter when no parameters are added"""
    from pyoracloud import ess

    sch_job = ess.SchedulerJob("package", "definition")
    assert sch_job.ess_parameter == ess.ESS_PARAM_NULL


def test_schedule_job_one_null_parameter() -> None:
    """ScheduleJob should include #NULL when None is added as parameter"""
    from pyoracloud import ess

    sch_job = ess.SchedulerJob("package", "definition")
    sch_job.add_parameter(None)
    sch_job.add_parameter("P1")
    sch_job.add_parameter(None)
    assert sch_job.ess_parameter == f"{ess.ESS_PARAM_NULL},P1,{ess.ESS_PARAM_NULL}"


def test_schedule_job_payload() -> None:
    """Validate the ScheduleJob payload"""
    from pyoracloud import ess

    package = "package"
    definition = "definition"
    parameter = "parameter"
    sch_job = ess.SchedulerJob(package, definition)
    sch_job.add_parameter(parameter)

    assert (
        sch_job.payload["OperationName"] == "submitESSJobRequest"
        and sch_job.payload["JobPackageName"] == package
        and sch_job.payload["JobDefName"] == definition
        and sch_job.payload["ESSParameters"] == parameter
        and sch_job.payload["ReqstId"] is None
        and len(sch_job.payload.keys()) == 5
    )


def test_enterprise_scheduler_accept_3_args() -> None:
    from pyoracloud.ess import EnterpriseScheduler

    url = "URL"
    username = "USERNAME"
    password = "PASSWORD"
    schdlr = EnterpriseScheduler(url, username, password)
    assert (
        schdlr.url == url
        and schdlr.username == username
        and schdlr.password == password
    )


def test_enterprise_scheduler_verbose() -> None:
    from pyoracloud.ess import EnterpriseScheduler

    schdlr = EnterpriseScheduler("x", "x", "x")
    assert schdlr.verbose == False
    schdlr.verbose = True
    assert schdlr.verbose == True


def test_enterprise_scheduler_max_poll() -> None:
    from pyoracloud.ess import EnterpriseScheduler

    schdlr = EnterpriseScheduler("x", "x", "x")
    assert schdlr.max_poll == 500


def test_enterprise_scheduler_poll_interval() -> None:
    from pyoracloud.ess import EnterpriseScheduler

    schdlr = EnterpriseScheduler("x", "x", "x")
    assert schdlr.poll_interval == 10


def test_enterprise_scheduler_progress_status() -> None:
    from pyoracloud.ess import EnterpriseScheduler

    schdlr = EnterpriseScheduler("x", "x", "x")
    assert all(
        [
            actual == expected
            for actual, expected in zip(
                schdlr.progress_status,
                ["WAIT", "BLOCKED", "RUNNING", "PAUSED", "COMPLETED", "READY"],
            )
        ]
    )


def test_enterprise_scheduler_erp_integration_url():
    from pyoracloud.ess import EnterpriseScheduler

    url = "https://server.oraclecloud.com"
    schdlr = EnterpriseScheduler(url, "x", "x")
    actual_url = f"{url}/fscmRestApi/resources/11.13.18.05/erpintegrations"

    assert actual_url == schdlr.erp_integration
