const nodes = [
    {id: 1, label: 'Tecnologia Takwara', shape: 'box', color: '#4CAF50', size: 30},
    {id: 2, label: 'Bambu', shape: 'ellipse', color: '#8BC34A'},
    {id: 3, label: 'PU Vegetal', shape: 'ellipse', color: '#8BC34A'},
    {id: 4, label: 'Forno Ecológico', shape: 'ellipse', color: '#CDDC39'},
    {id: 5, label: 'Conexões Geodésicas', shape: 'ellipse', color: '#CDDC39'}
];

const edges = [
    {from: 1, to: 2, arrows: 'to', label: 'usa'},
    {from: 1, to: 3, arrows: 'to', label: 'usa'},
    {from: 1, to: 4, arrows: 'to', label: 'inova com'},
    {from: 1, to: 5, arrows: 'to', label: 'inova com'},
    {from: 2, to: 4, arrows: 'to', label: 'é tratado em'},
    {from: 2, to: 5, arrows: 'to', label: 'é usado em'}
];