
Ext.onReady(function(){
    
    Ext.direct.Manager.addProvider(EXT_DIRECT_RPC_PROVIDER);

    function doEcho(field){
        Remote.TestAction.doEcho(field.getValue(), function(result, event){
            var transaction = event.getTransaction(),
                content = Ext.String.format('<b>Successful call to {0}.{1} with response:</b><pre>{2}</pre>',
                    transaction.action, transaction.method, Ext.encode(result));
            
            updateMain(content);
            field.reset();
        });
    }
    
    function doMultiply(field){
        Remote.TestAction.multiply(field.getValue(), function(result, event){
            var transaction = event.getTransaction(),
                content;
                
            if (event.status) {
                content = Ext.String.format('<b>Successful call to {0}.{1} with response:</b><pre>{2}</pre>',
                    transaction.action, transaction.method, Ext.encode(result));
            } else {
                content = Ext.String.format('<b>Call to {0}.{1} failed with message:</b><pre>{2}</pre>',
                    transaction.action, transaction.method, event.message);
            }
            updateMain(content);
            field.reset();
        });
    }
    
    var logger = Ext.create('Ext.panel.Panel', {
        title: 'Remote Call Log',
        renderTo: Ext.getBody(),
        width: 600,
        height: 300,
        tpl: '<p>{data}</p>',
        tplWriteMode: 'append',
        autoScroll: true,
        bodyStyle: 'padding: 5px;',
        dockedItems: [{
            dock: 'bottom',
            xtype: 'toolbar',
            items: [{
                hideLabel: true,
                itemId: 'echoText',
                xtype: 'textfield',
                width: 300,
                emptyText: 'Echo input',
                listeners: {
                    specialkey: function(field, event){
                        if (event.getKey() === event.ENTER) {
                            doEcho(field);
                        }
                    }
                }
            }, {
                itemId: 'echo',
                text: 'Echo',
                handler: function(){
                    doEcho(logger.down('#echoText'));
                }
            }, '-', {
                hideLabel: true,
                itemId: 'multiplyText',
                xtype: 'textfield',
                width: 80,
                emptyText: 'Multiply x 8',
                listeners: {
                    specialkey: function(field, event){
                        if (event.getKey() === event.ENTER) {
                            doMultiply(field);
                        }
                    }
                }
            }, {
                itemId: 'multiply',
                text: 'Multiply',
                handler: function(){
                    doMultiply(logger.down('#multiplyText'));
                }
            }]
        }]
    });
    
    function updateMain(content){
        logger.update({
            data: content
        });
        logger.body.scroll('b', 100000, true);
    }
});
