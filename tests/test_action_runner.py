import random
import pytest

from ImageCopy.Actions.exif_editing import ExifEditing
from ImageCopy.Transformers.grouping_transform import GroupingTransform
from ImageCopy.Transformers.raw_separate_transform import RawSeparateTransform
from ImageCopy.Transformers.rename_transform import RenameTransform
from ImageCopy.action_runner import ActionRunner
from tests.mock.mocks import MockConfig, MockTransformer, MockAction


class TestActionRunner:

    def test_invalid_config(self):
        with pytest.raises(ValueError):
            runner = ActionRunner(None)

    def test_tranformers_actions_not_created(self):
        mockConfig = MockConfig()
        runner = ActionRunner(mockConfig)
        assert len(runner.path_transformers) == 0
        assert len(runner.after_actions) == 0

    def test_transformers_actions_created(self):
        mockConfig = MockConfig(dict(), dict(), {"in": "", "out": ""}, dict())
        runner = ActionRunner(mockConfig)
        assert len(runner.path_transformers) == 3  # grouping, raw_separate, rename
        assert any(isinstance(transform, GroupingTransform) for transform in runner.path_transformers)
        assert any(isinstance(transform, RawSeparateTransform) for transform in runner.path_transformers)
        assert any(isinstance(transform, RenameTransform) for transform in runner.path_transformers)
        assert len(runner.after_actions) == 1  # exif
        assert len(runner.after_actions) == runner.get_after_action_count()
        assert any(isinstance(action, ExifEditing) for action in runner.after_actions)

    def test_executes_all_transformers(self):
        mockConfig = MockConfig()
        mockTransformers = [MockTransformer(), MockTransformer(), MockTransformer()]
        runner = ActionRunner(mockConfig)
        input_dict = {'test': True, 'x': 42}
        runner.path_transformers = mockTransformers
        runner.execute_transformers(input_dict)
        assert all(transform.transform_called for transform in mockTransformers)
        assert all(transform.transform_called_with == input_dict for transform in mockTransformers)

    def test_executes_all_transformers_randomized_amount(self):
        mockConfig = MockConfig()
        mockTransformers = [MockTransformer() for x in range(random.randint(1, 20))]
        runner = ActionRunner(mockConfig)
        input_dict = {'test': True, 'x': 42}
        runner.path_transformers = mockTransformers
        runner.execute_transformers(input_dict)
        assert all(transform.transform_called for transform in mockTransformers)
        assert all(transform.transform_called_with == input_dict for transform in mockTransformers)

    def test_executes_all_actions(self):
        mockConfig = MockConfig()
        mockActions = [MockAction(), MockAction()]
        runner = ActionRunner(mockConfig)
        input_dict = {'test': True, 'x': 42}
        runner.after_actions = mockActions
        runner.execute_after_actions(input_dict, lambda: None)
        assert all(action.execute_called for action in mockActions)
        assert all(action.execute_called_with == input_dict for action in mockActions)

    def test_executes_all_actions_randomized_amaount(self):
        mockConfig = MockConfig()
        mockActions = [MockAction() for x in range(random.randint(1, 20))]
        runner = ActionRunner(mockConfig)
        input_dict = {'test': True, 'x': 42}
        runner.after_actions = mockActions
        runner.execute_after_actions(input_dict, lambda: None)
        assert all(action.execute_called for action in mockActions)
        assert all(action.execute_called_with == input_dict for action in mockActions)

    def test_execute_actions_register_progress(self):

        class Counter:
            def __init__(self):
                self.progress_counter = 0

            def progress(self):
                self.progress_counter += 1

        mockConfig = MockConfig()
        mockActions = [MockAction() for x in range(random.randint(1, 20))]
        runner = ActionRunner(mockConfig)
        input_dict = {'test': True, 'x': 42}
        runner.after_actions = mockActions
        counter = Counter()
        runner.execute_after_actions(input_dict, counter.progress)
        assert counter.progress_counter == len(mockActions)
