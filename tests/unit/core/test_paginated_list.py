from luma_sdk.models.base import LumaModel
from luma_sdk.paginated_list import PaginatedList


class FakeModel(LumaModel):
    def __init__(self, data, requester):
        super().__init__(data, requester)
        self.id = data["api_id"]

    def __repr__(self):
        return f"<FakeModel id={self.id!r}>"


def make_requester(pages):
    """Returns a fake requester whose .get() yields pages in sequence."""
    call_count = [0]

    class FakeRequester:
        def get(self, path, parameters=None):
            page = pages[call_count[0]]
            call_count[0] += 1
            return page

    return FakeRequester()


def test_iterates_single_page():
    requester = make_requester([
        {"entries": [{"api_id": "a"}, {"api_id": "b"}], "has_more": False, "next_cursor": None},
    ])
    result = list(PaginatedList(requester, "/events", FakeModel))
    assert [e.id for e in result] == ["a", "b"]


def test_iterates_across_two_pages():
    requester = make_requester([
        {"entries": [{"api_id": "a"}], "has_more": True, "next_cursor": "cursor1"},
        {"entries": [{"api_id": "b"}], "has_more": False, "next_cursor": None},
    ])
    result = list(PaginatedList(requester, "/events", FakeModel))
    assert [e.id for e in result] == ["a", "b"]


def test_cursor_threaded_to_next_fetch():
    captured_params = []

    class FakeRequester:
        call = 0

        def get(self, path, parameters=None):
            captured_params.append(parameters or {})
            if self.call == 0:
                self.call += 1
                return {"entries": [{"api_id": "a"}], "has_more": True, "next_cursor": "cur1"}
            return {"entries": [{"api_id": "b"}], "has_more": False, "next_cursor": None}

    list(PaginatedList(FakeRequester(), "/events", FakeModel))
    assert "pagination_cursor" not in captured_params[0]
    assert captured_params[1]["pagination_cursor"] == "cur1"


def test_empty_first_page():
    requester = make_requester([
        {"entries": [], "has_more": False, "next_cursor": None},
    ])
    result = list(PaginatedList(requester, "/events", FakeModel))
    assert result == []


def test_params_passed_to_every_page():
    captured_params = []

    class FakeRequester:
        call = 0

        def get(self, path, parameters=None):
            captured_params.append(parameters or {})
            if self.call == 0:
                self.call += 1
                return {"entries": [{"api_id": "a"}], "has_more": True, "next_cursor": "c1"}
            return {"entries": [{"api_id": "b"}], "has_more": False, "next_cursor": None}

    list(PaginatedList(FakeRequester(), "/events", FakeModel, params={"sort_column": "start_at"}))
    assert captured_params[0]["sort_column"] == "start_at"
    assert captured_params[1]["sort_column"] == "start_at"
