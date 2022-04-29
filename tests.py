from mamba import description, it
from expects import expect, equal

from unittest.mock import Mock, patch

from main import CreateOrderHtmlResponse, CreateOrderService, OrderRepository, app


with description('test create order HTML representation adapter') as self:
    with it('returns success on truthy response'):
        expect(CreateOrderHtmlResponse().get_representation(True)).to(equal("<h1>Success</h1>"))
    with it('return "failed" on false response'):
        expect(CreateOrderHtmlResponse().get_representation(False)).to(equal("<h1>Failed</h1>"))

with description('test order repository') as self:
    with it('demonstrates mocking external dependency'):
        get_db_mock = Mock()
        with patch('main.get_db', get_db_mock):
            OrderRepository().create_order(random='args')
            get_db_mock.assert_called_once()

with description('test business logic'):
    with it('tests CreateOrderService with mocked repository'):
        create_order_mock = Mock()
        with patch('main.OrderRepository.create_order', create_order_mock):
            with app.app_context():
                result = CreateOrderService().create_order()
                expect(result).to(equal(True))
                create_order_mock.assert_called_once()

