import azq_server_api


def test():
    raised = False
    try:
        azq_server_api.api_login_get_token(
            "https://test0.azenqos.com/some_path", "wronguser", "wrongpass",
        )
    except Exception as exstr:
        raised = True
        print("exstr:", exstr)
        assert "Unauthorized" in str(exstr)

    assert raised == True
    print("test passed")


if __name__ == "__main__":
    test()
